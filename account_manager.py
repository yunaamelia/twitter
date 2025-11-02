"""
Twitter account manager for handling multiple accounts
"""
import tweepy
from typing import List, Optional, Dict
from config import Config
from models import Account, SessionLocal
from datetime import datetime
import logging
import time

logger = logging.getLogger(__name__)


class TwitterAccountManager:
    """Manage multiple Twitter accounts"""
    
    def __init__(self):
        self.accounts = {}  # account_number -> tweepy.Client
        self.account_info = {}  # account_number -> account details
        self.load_accounts()
    
    def load_accounts(self):
        """Load all configured Twitter accounts"""
        account_numbers = Config.get_all_account_numbers()
        
        logger.info(f"Loading {len(account_numbers)} Twitter accounts...")
        
        for account_num in account_numbers:
            try:
                creds = Config.get_account_credentials(account_num)
                
                # Create Twitter API client
                client = tweepy.Client(
                    bearer_token=Config.TWITTER_BEARER_TOKEN,
                    consumer_key=creds['api_key'],
                    consumer_secret=creds['api_secret'],
                    access_token=creds['access_token'],
                    access_token_secret=creds['access_secret'],
                    wait_on_rate_limit=True
                )
                
                # Verify credentials and get user info
                me = client.get_me()
                if me.data:
                    self.accounts[account_num] = client
                    self.account_info[account_num] = {
                        'id': me.data.id,
                        'username': me.data.username,
                        'name': me.data.name
                    }
                    
                    # Save to database
                    self._save_account_to_db(account_num, me.data.id, me.data.username)
                    
                    logger.info(f"Account {account_num} loaded: @{me.data.username}")
                else:
                    logger.error(f"Failed to verify account {account_num}")
                    
            except Exception as e:
                logger.error(f"Error loading account {account_num}: {e}")
        
        logger.info(f"Successfully loaded {len(self.accounts)} accounts")
    
    def _save_account_to_db(self, account_number: int, user_id: str, username: str):
        """Save account information to database"""
        db = SessionLocal()
        try:
            account = db.query(Account).filter_by(account_number=account_number).first()
            if not account:
                account = Account(
                    account_number=account_number,
                    user_id=user_id,
                    username=username
                )
                db.add(account)
            else:
                account.user_id = user_id
                account.username = username
            db.commit()
        finally:
            db.close()
    
    def get_account(self, account_number: int) -> Optional[tweepy.Client]:
        """Get a specific account client"""
        return self.accounts.get(account_number)
    
    def get_all_accounts(self) -> Dict[int, tweepy.Client]:
        """Get all account clients"""
        return self.accounts
    
    def get_active_accounts(self, limit: Optional[int] = None) -> List[int]:
        """Get list of active account numbers"""
        db = SessionLocal()
        try:
            query = db.query(Account).filter_by(is_active=True)
            if limit:
                query = query.limit(limit)
            accounts = query.all()
            return [acc.account_number for acc in accounts]
        finally:
            db.close()
    
    def follow_user(self, account_number: int, target_user_id: str) -> bool:
        """Follow a user with specific account"""
        try:
            client = self.get_account(account_number)
            if not client:
                return False
            
            client.follow_user(target_user_id)
            logger.info(f"Account {account_number} followed user {target_user_id}")
            time.sleep(2)  # Rate limiting
            return True
        except Exception as e:
            logger.error(f"Error following user: {e}")
            return False
    
    def retweet(self, account_number: int, tweet_id: str) -> bool:
        """Retweet with specific account"""
        try:
            client = self.get_account(account_number)
            if not client:
                return False
            
            client.retweet(tweet_id)
            logger.info(f"Account {account_number} retweeted {tweet_id}")
            time.sleep(2)  # Rate limiting
            return True
        except Exception as e:
            logger.error(f"Error retweeting: {e}")
            return False
    
    def like_tweet(self, account_number: int, tweet_id: str) -> bool:
        """Like a tweet with specific account"""
        try:
            client = self.get_account(account_number)
            if not client:
                return False
            
            client.like(tweet_id)
            logger.info(f"Account {account_number} liked {tweet_id}")
            time.sleep(2)  # Rate limiting
            return True
        except Exception as e:
            logger.error(f"Error liking tweet: {e}")
            return False
    
    def reply_to_tweet(self, account_number: int, tweet_id: str, text: str) -> bool:
        """Reply to a tweet with specific account"""
        try:
            client = self.get_account(account_number)
            if not client:
                return False
            
            client.create_tweet(text=text, in_reply_to_tweet_id=tweet_id)
            logger.info(f"Account {account_number} replied to {tweet_id}")
            time.sleep(2)  # Rate limiting
            return True
        except Exception as e:
            logger.error(f"Error replying to tweet: {e}")
            return False
    
    def update_account_stats(self, account_number: int, participated: bool = False, won: bool = False):
        """Update account statistics"""
        db = SessionLocal()
        try:
            account = db.query(Account).filter_by(account_number=account_number).first()
            if account:
                account.last_used = datetime.utcnow()
                if participated:
                    account.total_participations += 1
                if won:
                    account.total_wins += 1
                db.commit()
        finally:
            db.close()
