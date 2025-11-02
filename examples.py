"""
Example usage and testing script for Twitter Giveaway Bot
"""

def example_price_check():
    """Example: Check token prices"""
    print("=" * 60)
    print("Example: Checking Token Prices")
    print("=" * 60)
    
    from price_checker import PriceChecker
    
    pc = PriceChecker()
    
    tokens = ['BTC', 'ETH', 'BNB', 'SOL', 'DOGE']
    
    for token in tokens:
        price = pc.get_token_price(token)
        if price:
            print(f"{token}: ${price:,.2f}")
        else:
            print(f"{token}: Price not found")
    print()


def example_parse_giveaway():
    """Example: Parse giveaway rules"""
    print("=" * 60)
    print("Example: Parsing Giveaway Rules")
    print("=" * 60)
    
    from giveaway_parser import GiveawayParser
    
    gp = GiveawayParser()
    
    example_tweets = [
        "🎁 GIVEAWAY 🎁\nWin 100 BTC!\n✅ Follow @CryptoOrg\n✅ Retweet\n✅ Like\n✅ Tag 3 friends",
        "Free airdrop! 1000 ETH to 10 lucky winners! Just follow and RT!",
        "Join our token giveaway! Follow, like, and comment your wallet address!"
    ]
    
    for i, tweet in enumerate(example_tweets, 1):
        print(f"\nTweet {i}:")
        print(f"Text: {tweet[:50]}...")
        print(f"Is giveaway: {gp.is_giveaway_tweet(tweet)}")
        
        rules = gp.parse_rules(tweet)
        print(f"Rules: {rules}")
        
        if rules['comment']:
            comment = gp.generate_comment(tweet)
            print(f"Sample comment: {comment}")
    print()


def example_extract_token_info():
    """Example: Extract token information from text"""
    print("=" * 60)
    print("Example: Extracting Token Information")
    print("=" * 60)
    
    from price_checker import PriceChecker
    
    pc = PriceChecker()
    
    example_texts = [
        "Win 1000 DOGE! Follow and RT to enter!",
        "Giving away 0.5 BTC to one lucky winner!",
        "100 ETH giveaway! Don't miss out!",
    ]
    
    for text in example_texts:
        print(f"\nText: {text}")
        info = pc.extract_token_info(text)
        print(f"Token: {info['token_symbol']}")
        print(f"Price: ${info['token_price_usd']}" if info['token_price_usd'] else "Price: Unknown")
        if info['estimated_value_usd']:
            print(f"Estimated Value: ${info['estimated_value_usd']:,.2f}")
        print(f"Valuable: {pc.is_valuable_giveaway(info)}")
    print()


def example_database_queries():
    """Example: Database queries"""
    print("=" * 60)
    print("Example: Database Queries")
    print("=" * 60)
    
    from models import SessionLocal, Giveaway, Account, init_db
    
    init_db()
    db = SessionLocal()
    
    try:
        # Count records
        total_giveaways = db.query(Giveaway).count()
        total_accounts = db.query(Account).count()
        
        print(f"Total giveaways in database: {total_giveaways}")
        print(f"Total accounts in database: {total_accounts}")
        
        if total_giveaways > 0:
            print("\nRecent giveaways:")
            recent = db.query(Giveaway).order_by(
                Giveaway.created_at.desc()
            ).limit(5).all()
            
            for g in recent:
                print(f"  - @{g.author_username}: {g.token_symbol} (${g.token_price_usd})")
        
        if total_accounts > 0:
            print("\nAccount statistics:")
            accounts = db.query(Account).all()
            for acc in accounts[:5]:
                print(f"  - Account {acc.account_number}: {acc.total_participations} participations, {acc.total_wins} wins")
    
    finally:
        db.close()
    print()


def run_all_examples():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("Twitter Giveaway Bot - Examples")
    print("=" * 60 + "\n")
    
    try:
        example_price_check()
    except Exception as e:
        print(f"Price check example failed: {e}\n")
    
    try:
        example_parse_giveaway()
    except Exception as e:
        print(f"Parse giveaway example failed: {e}\n")
    
    try:
        example_extract_token_info()
    except Exception as e:
        print(f"Extract token info example failed: {e}\n")
    
    try:
        example_database_queries()
    except Exception as e:
        print(f"Database queries example failed: {e}\n")
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()
