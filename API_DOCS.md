# API & Architecture Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Main Bot (bot.py)                    │
│  - Orchestrates all components                          │
│  - Runs periodic cycles                                 │
└─────────────────────────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Account     │  │  Giveaway    │  │   Price      │
│  Manager     │  │  Parser      │  │   Checker    │
└──────────────┘  └──────────────┘  └──────────────┘
          │               │               │
          └───────────────┼───────────────┘
                          ▼
              ┌──────────────────────┐
              │  Database (SQLite)   │
              │  - Giveaways         │
              │  - Accounts          │
              │  - Notifications     │
              └──────────────────────┘
```

## Core Components

### 1. Bot (bot.py)

Main orchestrator that coordinates all bot activities.

**Key Methods:**

```python
class TwitterGiveawayBot:
    def search_giveaways() -> List[Dict]
        """Search Twitter for crypto giveaway tweets"""
        
    def participate_in_giveaways()
        """Participate in all pending giveaways"""
        
    def check_winners()
        """Check for winner announcements"""
        
    def run_cycle()
        """Run one complete bot cycle"""
        
    def get_statistics() -> Dict
        """Get bot statistics"""
```

### 2. Account Manager (account_manager.py)

Manages multiple Twitter accounts for participation.

**Key Methods:**

```python
class TwitterAccountManager:
    def load_accounts()
        """Load all configured Twitter accounts"""
        
    def get_account(account_number: int) -> tweepy.Client
        """Get a specific account client"""
        
    def follow_user(account_number: int, target_user_id: str) -> bool
        """Follow a user with specific account"""
        
    def retweet(account_number: int, tweet_id: str) -> bool
        """Retweet with specific account"""
        
    def like_tweet(account_number: int, tweet_id: str) -> bool
        """Like a tweet with specific account"""
        
    def reply_to_tweet(account_number: int, tweet_id: str, text: str) -> bool
        """Reply to a tweet with specific account"""
```

### 3. Price Checker (price_checker.py)

Verifies cryptocurrency token prices via CoinGecko API.

**Key Methods:**

```python
class PriceChecker:
    def get_token_price(token_symbol: str) -> Optional[float]
        """Get token price in USD"""
        
    def extract_token_info(text: str) -> Dict[str, any]
        """Extract token information from giveaway text"""
        
    def is_valuable_giveaway(token_info: Dict) -> bool
        """Check if giveaway meets minimum value requirements"""
```

### 4. Giveaway Parser (giveaway_parser.py)

Parses giveaway tweets and extracts participation rules.

**Key Methods:**

```python
class GiveawayParser:
    def is_giveaway_tweet(text: str) -> bool
        """Check if tweet is a giveaway"""
        
    def parse_rules(text: str) -> Dict[str, bool]
        """Parse giveaway rules from tweet text"""
        
    def generate_comment(text: str) -> str
        """Generate an appropriate comment for the giveaway"""
        
    def should_participate(tweet_data: Dict, token_info: Dict) -> bool
        """Determine if bot should participate in this giveaway"""
```

### 5. Winner Detector (winner_detector.py)

Monitors for winner announcements via DMs and mentions.

**Key Methods:**

```python
class WinnerDetector:
    def check_for_winners()
        """Check all accounts for winner notifications"""
        
    def get_recent_wins(days: int = 7) -> List[Dict]
        """Get recent wins from all accounts"""
```

## Database Schema

### Giveaways Table

```sql
CREATE TABLE giveaways (
    id INTEGER PRIMARY KEY,
    tweet_id VARCHAR(50) UNIQUE NOT NULL,
    author_id VARCHAR(50) NOT NULL,
    author_username VARCHAR(100) NOT NULL,
    tweet_text TEXT NOT NULL,
    token_name VARCHAR(100),
    token_symbol VARCHAR(20),
    token_price_usd FLOAT,
    estimated_value_usd FLOAT,
    created_at DATETIME,
    deadline DATETIME,
    participated BOOLEAN DEFAULT FALSE,
    followed BOOLEAN DEFAULT FALSE,
    retweeted BOOLEAN DEFAULT FALSE,
    liked BOOLEAN DEFAULT FALSE,
    commented BOOLEAN DEFAULT FALSE,
    won BOOLEAN DEFAULT FALSE,
    winner_announced BOOLEAN DEFAULT FALSE,
    checked_at DATETIME
);
```

### Accounts Table

```sql
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY,
    account_number INTEGER UNIQUE NOT NULL,
    username VARCHAR(100),
    user_id VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    last_used DATETIME,
    total_participations INTEGER DEFAULT 0,
    total_wins INTEGER DEFAULT 0,
    created_at DATETIME
);
```

### Winner Notifications Table

```sql
CREATE TABLE winner_notifications (
    id INTEGER PRIMARY KEY,
    giveaway_id INTEGER,
    account_number INTEGER,
    notification_type VARCHAR(20),
    notification_text TEXT,
    received_at DATETIME,
    processed BOOLEAN DEFAULT FALSE
);
```

## Bot Workflow

### 1. Initialization

```
1. Load environment variables from .env
2. Initialize database (create tables if needed)
3. Load all configured Twitter accounts
4. Verify account credentials
5. Initialize price checker with CoinGecko API
```

### 2. Search Phase

```
For each search query:
  1. Search Twitter for recent tweets (last 24h)
  2. Filter out retweets
  3. Get tweet metadata (author, metrics, etc.)
  4. Extract token information
  5. Verify token has real price
  6. Check if meets minimum thresholds
  7. Save to database if valid
```

### 3. Participation Phase

```
For each pending giveaway:
  1. Parse giveaway rules (follow, retweet, like, comment)
  2. Get list of active accounts
  3. For each account:
     a. Perform required actions (follow, retweet, etc.)
     b. Add delays between actions (rate limiting)
     c. Update account statistics
  4. Mark giveaway as participated
  5. Log results
```

### 4. Winner Detection Phase

```
For each active account:
  1. Check Twitter mentions (last 24h)
  2. Look for winner-related keywords
  3. Save winner notifications to database
  4. Update giveaway won status
  5. Update account win statistics
```

## Rate Limiting Strategy

### Twitter API Limits

- **Search**: 180 requests / 15 minutes
- **User Timeline**: 900 requests / 15 minutes
- **Follow/Retweet/Like**: Various per account

### Bot Rate Limiting

```python
# Between actions on same account
time.sleep(2)  # 2 seconds

# Between different accounts
time.sleep(5)  # 5 seconds

# Between giveaways
time.sleep(10)  # 10 seconds

# Between search cycles
CHECK_INTERVAL_MINUTES = 15  # 15 minutes (configurable)
```

## Configuration Parameters

### Required Parameters

```bash
TWITTER_BEARER_TOKEN          # Main API bearer token
TWITTER_API_KEY_N             # API key for account N
TWITTER_API_SECRET_N          # API secret for account N
TWITTER_ACCESS_TOKEN_N        # Access token for account N
TWITTER_ACCESS_SECRET_N       # Access secret for account N
```

### Optional Parameters

```bash
MIN_TOKEN_PRICE_USD=0.01               # Minimum token price
MAX_ACCOUNTS_TO_USE=100                # Max accounts per giveaway
CHECK_INTERVAL_MINUTES=15              # Check frequency
MIN_FOLLOWERS_REQUIRED=1000            # Min organizer followers
MIN_GIVEAWAY_VALUE_USD=50              # Min giveaway value
COINGECKO_API_KEY=optional_key         # For better price data
DATABASE_URL=sqlite:///giveaways.db    # Database location
```

## Error Handling

### Network Errors

- Automatic retry with exponential backoff
- Wait on rate limit (built into tweepy)
- Log all errors to bot.log

### Authentication Errors

- Skip problematic accounts
- Continue with remaining accounts
- Log authentication failures

### Database Errors

- Use transactions for consistency
- Rollback on failures
- Prevent duplicate entries

## Logging

### Log Levels

- **INFO**: Normal operations, cycle completion
- **DEBUG**: Detailed processing steps
- **WARNING**: Rate limits, missing data
- **ERROR**: Failed operations, API errors

### Log Format

```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
2024-01-01 12:00:00 - bot - INFO - Starting bot cycle...
```

### Log Files

- `bot.log`: All bot activities
- Console output: Real-time monitoring

## Extension Points

### Adding New Token Price Sources

Extend `price_checker.py`:

```python
def _get_price_from_custom_api(self, token_symbol: str) -> Optional[float]:
    # Implement custom price API
    pass
```

### Custom Giveaway Filters

Extend `giveaway_parser.py`:

```python
def custom_filter(self, tweet_data: Dict) -> bool:
    # Implement custom filtering logic
    pass
```

### Custom Comment Generation

Edit `giveaway_parser.py`:

```python
def generate_comment(self, text: str) -> str:
    # Use AI or custom templates
    pass
```

## Performance Optimization

### Database Indexing

```python
# Already implemented
tweet_id: unique index
account_number: unique index
created_at: for time-based queries
```

### Caching

```python
# Price cache in PriceChecker
self.cache = {}  # token_symbol -> price_usd
```

### Connection Pooling

```python
# SQLAlchemy handles connection pooling automatically
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

## Security Considerations

### Credential Storage

- Never commit .env file
- Use environment variables
- Rotate API keys regularly

### API Key Protection

- Separate keys per account group
- Monitor for unauthorized usage
- Use least privilege principle

### Rate Limit Compliance

- Built-in delays
- Respects Twitter TOS
- Automatic rate limit handling

## Monitoring & Maintenance

### Daily Tasks

```bash
# Check bot status
python stats.py

# View logs
tail -f bot.log

# Verify accounts
python setup_verify.py
```

### Weekly Tasks

- Review win rates
- Check account health
- Update token mappings
- Optimize filters

### Monthly Tasks

- Update dependencies
- Review and rotate API keys
- Analyze performance metrics
- Adjust configuration

## Testing

### Manual Testing

```bash
# Verify setup
python setup_verify.py

# Check statistics
python stats.py

# Test single cycle (modify main.py to exit after one cycle)
python main.py
```

### Component Testing

```python
# Test price checker
from price_checker import PriceChecker
pc = PriceChecker()
print(pc.get_token_price('BTC'))

# Test giveaway parser
from giveaway_parser import GiveawayParser
gp = GiveawayParser()
print(gp.is_giveaway_tweet("Win 100 BTC! Follow and RT!"))
```

## Troubleshooting Guide

### Common Issues

1. **No giveaways found**
   - Lower MIN_TOKEN_PRICE_USD
   - Check search queries
   - Verify API access

2. **Rate limit errors**
   - Increase delays
   - Reduce account usage
   - Wait for limit reset

3. **Authentication failures**
   - Verify credentials
   - Check account status
   - Regenerate tokens

4. **Database locked**
   - Only one bot instance
   - Check file permissions
   - Restart bot

## Support & Resources

- GitHub Issues: Report bugs and request features
- Documentation: README.md, QUICKSTART.md
- Logs: bot.log for detailed troubleshooting
- Community: Contribute improvements

---

**Last Updated**: 2024
**Version**: 1.0.0
