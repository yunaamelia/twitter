"""
Main bot orchestrator
"""
import tweepy
from typing import List, Dict
from datetime import datetime, timedelta
import logging
import time

from config import Config
from models import Giveaway, SessionLocal, init_db
from account_manager import TwitterAccountManager
from price_checker import PriceChecker
from giveaway_parser import GiveawayParser
from winner_detector import WinnerDetector

logger = logging.getLogger(__name__)


class TwitterGiveawayBot:
    """Main bot class for finding and participating in crypto giveaways"""
    
    def __init__(self):
        logger.info("Initializing Twitter Giveaway Bot...")
        
        # Initialize database
        init_db()
        
        # Initialize components
        self.account_manager = TwitterAccountManager()
        self.price_checker = PriceChecker()
        self.giveaway_parser = GiveawayParser()
        self.winner_detector = WinnerDetector(self.account_manager)
        
        # Create search client using bearer token
        self.search_client = tweepy.Client(
            bearer_token=Config.TWITTER_BEARER_TOKEN,
            wait_on_rate_limit=True
        )
        
        logger.info("Bot initialized successfully!")
    
    def search_giveaways(self) -> List[Dict]:
        """Search for crypto giveaway tweets"""
        logger.info("Searching for crypto giveaways...")
        
        giveaways = []
        
        # Build search queries
        queries = self._build_search_queries()
        
        for query in queries:
            try:
                logger.info(f"Searching with query: {query}")
                
                # Search tweets from last 24 hours
                end_time = datetime.utcnow()
                start_time = end_time - timedelta(hours=24)
                
                tweets = self.search_client.search_recent_tweets(
                    query=query,
                    max_results=100,
                    start_time=start_time.isoformat() + 'Z',
                    tweet_fields=['created_at', 'author_id', 'public_metrics', 'text'],
                    user_fields=['username', 'public_metrics'],
                    expansions=['author_id']
                )
                
                if not tweets.data:
                    continue
                
                # Process tweets
                users_dict = {user.id: user for user in tweets.includes.get('users', [])}
                
                for tweet in tweets.data:
                    author = users_dict.get(tweet.author_id)
                    if not author:
                        continue
                    
                    tweet_data = {
                        'id': tweet.id,
                        'text': tweet.text,
                        'author_id': tweet.author_id,
                        'author_username': author.username,
                        'author_followers': author.public_metrics.get('followers_count', 0),
                        'created_at': tweet.created_at,
                        'retweet_count': tweet.public_metrics.get('retweet_count', 0),
                        'like_count': tweet.public_metrics.get('like_count', 0)
                    }
                    
                    # Check if it's a valid giveaway
                    if self._process_potential_giveaway(tweet_data):
                        giveaways.append(tweet_data)
                
                # Rate limiting
                time.sleep(5)
                
            except Exception as e:
                logger.error(f"Error searching with query '{query}': {e}")
        
        logger.info(f"Found {len(giveaways)} potential giveaways")
        return giveaways
    
    def _build_search_queries(self) -> List[str]:
        """Build Twitter search queries for crypto giveaways"""
        queries = [
            "crypto giveaway -is:retweet lang:en",
            "token giveaway -is:retweet lang:en",
            "BTC giveaway -is:retweet lang:en",
            "ETH giveaway -is:retweet lang:en",
            "crypto airdrop -is:retweet lang:en",
            "win crypto -is:retweet lang:en",
        ]
        return queries
    
    def _process_potential_giveaway(self, tweet_data: Dict) -> bool:
        """Process a potential giveaway tweet"""
        try:
            # Check if already in database
            db = SessionLocal()
            existing = db.query(Giveaway).filter_by(tweet_id=tweet_data['id']).first()
            db.close()
            
            if existing:
                return False
            
            # Extract token information
            token_info = self.price_checker.extract_token_info(tweet_data['text'])
            
            # Check if it's a valuable giveaway
            if not self.price_checker.is_valuable_giveaway(token_info):
                logger.debug(f"Tweet {tweet_data['id']} doesn't meet value requirements")
                return False
            
            # Check if we should participate
            if not self.giveaway_parser.should_participate(tweet_data, token_info):
                logger.debug(f"Tweet {tweet_data['id']} doesn't meet participation criteria")
                return False
            
            # Save to database
            self._save_giveaway(tweet_data, token_info)
            
            return True
            
        except Exception as e:
            logger.error(f"Error processing tweet {tweet_data.get('id')}: {e}")
            return False
    
    def _save_giveaway(self, tweet_data: Dict, token_info: Dict):
        """Save giveaway to database"""
        db = SessionLocal()
        try:
            giveaway = Giveaway(
                tweet_id=tweet_data['id'],
                author_id=tweet_data['author_id'],
                author_username=tweet_data['author_username'],
                tweet_text=tweet_data['text'],
                token_name=token_info.get('token_name'),
                token_symbol=token_info.get('token_symbol'),
                token_price_usd=token_info.get('token_price_usd'),
                estimated_value_usd=token_info.get('estimated_value_usd')
            )
            db.add(giveaway)
            db.commit()
            logger.info(f"Saved giveaway {tweet_data['id']} to database")
        finally:
            db.close()
    
    def participate_in_giveaways(self):
        """Participate in all pending giveaways"""
        logger.info("Participating in giveaways...")
        
        db = SessionLocal()
        try:
            # Get giveaways that haven't been participated in yet
            pending = db.query(Giveaway).filter_by(participated=False).all()
            
            logger.info(f"Found {len(pending)} pending giveaways")
            
            for giveaway in pending:
                try:
                    self._participate_in_giveaway(giveaway)
                    time.sleep(10)  # Rate limiting between giveaways
                except Exception as e:
                    logger.error(f"Error participating in giveaway {giveaway.tweet_id}: {e}")
            
        finally:
            db.close()
    
    def _participate_in_giveaway(self, giveaway: Giveaway):
        """Participate in a single giveaway with multiple accounts"""
        logger.info(f"Participating in giveaway: {giveaway.tweet_id}")
        
        # Parse rules
        rules = self.giveaway_parser.parse_rules(giveaway.tweet_text)
        logger.info(f"Rules: {rules}")
        
        # Get active accounts to use
        active_accounts = self.account_manager.get_active_accounts(
            limit=Config.MAX_ACCOUNTS_TO_USE
        )
        
        if not active_accounts:
            logger.error("No active accounts available!")
            return
        
        participated_count = 0
        
        # Participate with multiple accounts
        for account_num in active_accounts:
            try:
                success = True
                
                # Follow
                if rules['follow']:
                    success &= self.account_manager.follow_user(
                        account_num, 
                        giveaway.author_id
                    )
                    giveaway.followed = True
                
                # Retweet
                if rules['retweet']:
                    success &= self.account_manager.retweet(
                        account_num,
                        giveaway.tweet_id
                    )
                    giveaway.retweeted = True
                
                # Like
                if rules['like']:
                    success &= self.account_manager.like_tweet(
                        account_num,
                        giveaway.tweet_id
                    )
                    giveaway.liked = True
                
                # Comment
                if rules['comment']:
                    comment_text = self.giveaway_parser.generate_comment(giveaway.tweet_text)
                    success &= self.account_manager.reply_to_tweet(
                        account_num,
                        giveaway.tweet_id,
                        comment_text
                    )
                    giveaway.commented = True
                
                if success:
                    participated_count += 1
                    self.account_manager.update_account_stats(account_num, participated=True)
                
                # Rate limiting between accounts
                time.sleep(5)
                
            except Exception as e:
                logger.error(f"Error with account {account_num}: {e}")
        
        # Update giveaway status
        db = SessionLocal()
        try:
            db_giveaway = db.query(Giveaway).filter_by(id=giveaway.id).first()
            if db_giveaway:
                db_giveaway.participated = True
                db_giveaway.followed = giveaway.followed
                db_giveaway.retweeted = giveaway.retweeted
                db_giveaway.liked = giveaway.liked
                db_giveaway.commented = giveaway.commented
                db.commit()
        finally:
            db.close()
        
        logger.info(f"Participated with {participated_count} accounts")
    
    def check_winners(self):
        """Check for winner announcements"""
        logger.info("Checking for winners...")
        self.winner_detector.check_for_winners()
    
    def run_cycle(self):
        """Run one complete bot cycle"""
        logger.info("=" * 50)
        logger.info("Starting bot cycle...")
        logger.info("=" * 50)
        
        try:
            # Step 1: Search for new giveaways
            self.search_giveaways()
            
            # Step 2: Participate in pending giveaways
            self.participate_in_giveaways()
            
            # Step 3: Check for winner notifications
            self.check_winners()
            
            logger.info("Bot cycle completed successfully!")
            
        except Exception as e:
            logger.error(f"Error in bot cycle: {e}")
    
    def get_statistics(self) -> Dict:
        """Get bot statistics"""
        db = SessionLocal()
        try:
            total_giveaways = db.query(Giveaway).count()
            participated = db.query(Giveaway).filter_by(participated=True).count()
            wins = db.query(Giveaway).filter_by(won=True).count()
            
            from models import Account
            active_accounts = db.query(Account).filter_by(is_active=True).count()
            
            return {
                'total_giveaways_found': total_giveaways,
                'total_participations': participated,
                'total_wins': wins,
                'active_accounts': active_accounts,
                'win_rate': f"{(wins/participated*100):.2f}%" if participated > 0 else "0%"
            }
        finally:
            db.close()
