"""
Configuration management for Twitter Giveaway Bot
"""
import os
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()


class Config:
    """Bot configuration"""
    
    # Bot settings
    MIN_TOKEN_PRICE_USD = float(os.getenv('MIN_TOKEN_PRICE_USD', '0.01'))
    MAX_ACCOUNTS_TO_USE = int(os.getenv('MAX_ACCOUNTS_TO_USE', '100'))
    CHECK_INTERVAL_MINUTES = int(os.getenv('CHECK_INTERVAL_MINUTES', '15'))
    MIN_FOLLOWERS_REQUIRED = int(os.getenv('MIN_FOLLOWERS_REQUIRED', '1000'))
    MIN_GIVEAWAY_VALUE_USD = float(os.getenv('MIN_GIVEAWAY_VALUE_USD', '50'))
    
    # Twitter API
    TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
    
    # CoinGecko API
    COINGECKO_API_KEY = os.getenv('COINGECKO_API_KEY')
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///giveaways.db')
    
    # Search keywords for crypto giveaways
    CRYPTO_KEYWORDS = [
        'giveaway', 'airdrop', 'free crypto', 'free tokens',
        'win crypto', 'win tokens', 'crypto contest', 'token giveaway'
    ]
    
    # Token/coin related keywords
    TOKEN_KEYWORDS = [
        'BTC', 'ETH', 'USDT', 'BNB', 'SOL', 'ADA', 'XRP', 'DOGE',
        'bitcoin', 'ethereum', 'crypto', 'token', 'coin', 'cryptocurrency'
    ]
    
    # Giveaway action keywords
    ACTION_KEYWORDS = {
        'follow': ['follow', 'following', 'follow us', 'follow @'],
        'retweet': ['retweet', 'rt', 'share', 'repost'],
        'like': ['like', 'heart', '❤️', '♥'],
        'comment': ['comment', 'reply', 'tag', 'mention']
    }
    
    @staticmethod
    def get_account_credentials(account_number: int) -> Dict[str, str]:
        """Get credentials for a specific account number"""
        return {
            'api_key': os.getenv(f'TWITTER_API_KEY_{account_number}'),
            'api_secret': os.getenv(f'TWITTER_API_SECRET_{account_number}'),
            'access_token': os.getenv(f'TWITTER_ACCESS_TOKEN_{account_number}'),
            'access_secret': os.getenv(f'TWITTER_ACCESS_SECRET_{account_number}')
        }
    
    @staticmethod
    def get_all_account_numbers() -> List[int]:
        """Get all configured account numbers"""
        accounts = []
        for i in range(1, Config.MAX_ACCOUNTS_TO_USE + 1):
            creds = Config.get_account_credentials(i)
            if all(creds.values()):
                accounts.append(i)
        return accounts
