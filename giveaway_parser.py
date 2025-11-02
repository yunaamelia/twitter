"""
Giveaway detector and parser
"""
import re
from typing import Optional, Dict, List
from config import Config
import logging

logger = logging.getLogger(__name__)


class GiveawayParser:
    """Parse giveaway tweets and extract rules"""
    
    def __init__(self):
        self.action_keywords = Config.ACTION_KEYWORDS
    
    def is_giveaway_tweet(self, text: str) -> bool:
        """
        Check if tweet is a giveaway
        
        Args:
            text: Tweet text
            
        Returns:
            True if tweet appears to be a giveaway
        """
        text_lower = text.lower()
        
        # Check for giveaway keywords
        giveaway_indicators = ['giveaway', 'airdrop', 'win', 'contest', 'free']
        has_giveaway = any(keyword in text_lower for keyword in giveaway_indicators)
        
        if not has_giveaway:
            return False
        
        # Check for crypto-related keywords
        crypto_indicators = [
            'btc', 'eth', 'crypto', 'token', 'coin', 'usdt', 'bnb', 
            'sol', 'ada', 'xrp', 'doge', 'bitcoin', 'ethereum', 'cryptocurrency'
        ]
        has_crypto = any(keyword in text_lower for keyword in crypto_indicators)
        
        return has_crypto
    
    def parse_rules(self, text: str) -> Dict[str, bool]:
        """
        Parse giveaway rules from tweet text
        
        Args:
            text: Tweet text
            
        Returns:
            Dictionary with required actions: follow, retweet, like, comment
        """
        text_lower = text.lower()
        
        rules = {
            'follow': False,
            'retweet': False,
            'like': False,
            'comment': False
        }
        
        # Check for follow requirement
        follow_patterns = [
            r'follow\s+@?\w+',
            r'follow\s+us',
            r'following\s+@?\w+',
            r'must\s+follow',
            r'✅\s*follow',
            r'1\.\s*follow',
        ]
        for pattern in follow_patterns:
            if re.search(pattern, text_lower):
                rules['follow'] = True
                break
        
        # Check for retweet requirement
        retweet_patterns = [
            r'\bretweet\b',
            r'\brt\b',
            r'share\s+this',
            r'repost',
            r'✅\s*retweet',
            r'2\.\s*retweet',
            r'🔁'
        ]
        for pattern in retweet_patterns:
            if re.search(pattern, text_lower):
                rules['retweet'] = True
                break
        
        # Check for like requirement
        like_patterns = [
            r'\blike\b',
            r'heart',
            r'❤️',
            r'♥',
            r'✅\s*like',
            r'3\.\s*like',
        ]
        for pattern in like_patterns:
            if re.search(pattern, text_lower):
                rules['like'] = True
                break
        
        # Check for comment/reply requirement
        comment_patterns = [
            r'\bcomment\b',
            r'\breply\b',
            r'tag\s+\d+\s+friends',
            r'mention\s+\d+',
            r'✅\s*comment',
            r'4\.\s*comment',
            r'💬'
        ]
        for pattern in comment_patterns:
            if re.search(pattern, text_lower):
                rules['comment'] = True
                break
        
        return rules
    
    def extract_mentioned_accounts(self, text: str) -> List[str]:
        """
        Extract @mentioned accounts from tweet text
        
        Args:
            text: Tweet text
            
        Returns:
            List of usernames (without @)
        """
        # Find all @mentions
        mentions = re.findall(r'@(\w+)', text)
        return mentions
    
    def extract_deadline(self, text: str) -> Optional[str]:
        """
        Extract giveaway deadline from text
        
        Args:
            text: Tweet text
            
        Returns:
            Deadline string if found
        """
        deadline_patterns = [
            r'ends?\s+on\s+(\w+\s+\d+)',
            r'until\s+(\w+\s+\d+)',
            r'deadline[:\s]+(\w+\s+\d+)',
            r'(\d+)\s+days?',
            r'(\d+)\s+hours?',
        ]
        
        for pattern in deadline_patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(1)
        
        return None
    
    def generate_comment(self, text: str) -> str:
        """
        Generate an appropriate comment for the giveaway
        
        Args:
            text: Original tweet text
            
        Returns:
            Comment text
        """
        comments = [
            "🚀 Great project! Count me in!",
            "🔥 Amazing giveaway! Thanks for the opportunity!",
            "💎 This looks promising! Let's go!",
            "⭐ Excited to participate!",
            "🎉 Love this project! To the moon!",
            "✨ Thanks for this opportunity!",
            "🌟 Amazing initiative!",
            "💯 Let's gooo!",
            "🙌 Great community!",
            "🎊 Participating! Good luck everyone!",
        ]
        
        import random
        return random.choice(comments)
    
    def should_participate(self, tweet_data: Dict, token_info: Dict) -> bool:
        """
        Determine if bot should participate in this giveaway
        
        Args:
            tweet_data: Tweet information
            token_info: Token information from price checker
            
        Returns:
            True if bot should participate
        """
        # Check if it's a giveaway
        if not self.is_giveaway_tweet(tweet_data.get('text', '')):
            return False
        
        # Check token price requirement
        if not token_info.get('token_price_usd'):
            logger.debug("No token price found, skipping")
            return False
        
        if token_info['token_price_usd'] < Config.MIN_TOKEN_PRICE_USD:
            logger.debug(f"Token price too low: ${token_info['token_price_usd']}")
            return False
        
        # Check author followers count
        author_followers = tweet_data.get('author_followers', 0)
        if author_followers < Config.MIN_FOLLOWERS_REQUIRED:
            logger.debug(f"Author has too few followers: {author_followers}")
            return False
        
        return True
