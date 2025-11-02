"""
Setup script to verify configuration and test API connections
"""
import os
from dotenv import load_dotenv
import tweepy
from config import Config

load_dotenv()


def check_environment():
    """Check if .env file exists and is configured"""
    print("🔍 Checking environment configuration...")
    
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("   Please copy .env.example to .env and configure it.")
        return False
    
    print("✅ .env file found")
    return True


def check_bearer_token():
    """Check if bearer token is configured and valid"""
    print("\n🔑 Checking Twitter Bearer Token...")
    
    bearer_token = Config.TWITTER_BEARER_TOKEN
    if not bearer_token or bearer_token == "your_bearer_token_here":
        print("❌ Bearer token not configured!")
        print("   Please set TWITTER_BEARER_TOKEN in .env")
        return False
    
    try:
        client = tweepy.Client(bearer_token=bearer_token)
        # Try a simple request
        result = client.search_recent_tweets(query="test", max_results=10)
        print("✅ Bearer token is valid!")
        return True
    except Exception as e:
        print(f"❌ Bearer token test failed: {e}")
        return False


def check_accounts():
    """Check configured Twitter accounts"""
    print("\n👥 Checking Twitter account configurations...")
    
    account_numbers = Config.get_all_account_numbers()
    
    if not account_numbers:
        print("❌ No accounts configured!")
        print("   Please add at least one account configuration to .env")
        return False
    
    print(f"📊 Found {len(account_numbers)} configured account(s)")
    
    valid_accounts = 0
    for account_num in account_numbers[:5]:  # Test first 5 accounts
        try:
            creds = Config.get_account_credentials(account_num)
            
            client = tweepy.Client(
                bearer_token=Config.TWITTER_BEARER_TOKEN,
                consumer_key=creds['api_key'],
                consumer_secret=creds['api_secret'],
                access_token=creds['access_token'],
                access_token_secret=creds['access_secret']
            )
            
            me = client.get_me()
            if me.data:
                print(f"  ✅ Account {account_num}: @{me.data.username}")
                valid_accounts += 1
            else:
                print(f"  ❌ Account {account_num}: Failed to verify")
                
        except Exception as e:
            print(f"  ❌ Account {account_num}: {str(e)[:50]}")
    
    if len(account_numbers) > 5:
        print(f"  ... and {len(account_numbers) - 5} more accounts")
    
    print(f"\n✅ {valid_accounts}/{min(len(account_numbers), 5)} test accounts verified")
    return valid_accounts > 0


def check_database():
    """Check database configuration"""
    print("\n💾 Checking database configuration...")
    
    from models import init_db, engine
    
    try:
        init_db()
        print("✅ Database initialized successfully!")
        print(f"   Database URL: {Config.DATABASE_URL}")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False


def check_dependencies():
    """Check if all dependencies are installed"""
    print("\n📦 Checking dependencies...")
    
    required = [
        ('tweepy', 'tweepy'),
        ('requests', 'requests'),
        ('python-dotenv', 'dotenv'),
        ('schedule', 'schedule'),
        ('pycoingecko', 'pycoingecko'),
        ('sqlalchemy', 'sqlalchemy'),
    ]
    
    missing = []
    for package_name, import_name in required:
        try:
            __import__(import_name)
            print(f"  ✅ {package_name}")
        except ImportError:
            print(f"  ❌ {package_name}")
            missing.append(package_name)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies installed!")
    return True


def main():
    """Main setup verification"""
    print("=" * 60)
    print("Twitter Giveaway Bot - Setup Verification")
    print("=" * 60)
    
    checks = [
        check_dependencies(),
        check_environment(),
        check_bearer_token(),
        check_accounts(),
        check_database(),
    ]
    
    print("\n" + "=" * 60)
    if all(checks):
        print("✅ All checks passed! You're ready to run the bot.")
        print("\nTo start the bot, run:")
        print("  python main.py")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nFor help, check README.md or visit:")
        print("  https://github.com/benihutapea/twitterga")
    print("=" * 60)


if __name__ == "__main__":
    main()
