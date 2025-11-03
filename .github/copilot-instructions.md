# Twitter Giveaway Bot - AI Coding Agent Instructions

## Project Overview

This is a production-ready Twitter bot that automatically discovers crypto giveaways, verifies token prices, participates with 100+ accounts, and monitors for wins. Built with Python 3.8+, Tweepy v2 API, SQLAlchemy, and CoinGecko API integration.

**Architecture**: Component-based design with clear separation: `bot.py` orchestrates, `account_manager.py` handles multi-account operations, `price_checker.py` verifies token value, `giveaway_parser.py` extracts rules, `winner_detector.py` monitors notifications.

## Critical Patterns & Conventions

### 1. Configuration Management (`config.py`)
- **All settings via environment variables** - Never hardcode credentials or thresholds
- Account credentials use numbered suffix pattern: `TWITTER_API_KEY_1`, `TWITTER_API_KEY_2`, etc.
- Use `Config.get_account_credentials(n)` to retrieve account-specific credentials
- All rate limits, thresholds, and intervals are configurable via `.env`

### 2. Database Operations (`models.py`)
- **Always use context managers** for database sessions:
  ```python
  db = SessionLocal()
  try:
      # operations
      db.commit()
  finally:
      db.close()
  ```
- Three core tables: `Giveaway` (tweet data + participation tracking), `Account` (account stats), `WinnerNotification` (win tracking)
- Check for duplicates before inserting: query by `tweet_id` (unique) or `account_number` (unique)

### 3. Rate Limiting Strategy
- **Built-in delays between actions**: 2s between actions on same account, 5s between different accounts, 10s between giveaways
- Tweepy clients initialized with `wait_on_rate_limit=True` - automatic handling of Twitter API limits
- Search cycles run at `Config.CHECK_INTERVAL_MINUTES` (default 15 min) via `schedule` library in `main.py`
- Never remove time.sleep() calls - they prevent API bans

### 4. Multi-Account Management (`account_manager.py`)
- Accounts loaded at startup via `load_accounts()` - verifies credentials and stores user info
- Each account gets individual `tweepy.Client` instance with both bearer token (search) and user auth (actions)
- Methods return `bool` for success/failure - always check return values
- `update_account_stats()` tracks participations and wins - call after each action

### 5. Error Handling & Logging
- Use module-level logger: `logger = logging.getLogger(__name__)`
- Log levels: DEBUG for detailed steps, INFO for operations, WARNING for rate limits, ERROR for failures
- All API calls wrapped in try/except - log errors but continue processing remaining items
- Logs written to both `bot.log` (file) and stdout (console)

### 6. Twitter API v2 Specifics
- Search uses bearer token client: `self.search_client = tweepy.Client(bearer_token=...)`
- Actions (follow/RT/like/reply) use user-context clients with OAuth 1.0a credentials
- Search queries use `-is:retweet lang:en` to filter, `max_results=100` for pagination
- Tweet fields pattern: `tweet_fields=['created_at', 'author_id', 'public_metrics', 'text']`
- Always include `expansions=['author_id']` to get user data with tweets

### 7. Token Price Verification (`price_checker.py`)
- Symbol mapping dictionary for common tokens (BTC→bitcoin, ETH→ethereum, etc.)
- Fallback to CoinGecko search if symbol not in mapping
- Simple in-memory cache (`self.cache`) to reduce API calls
- Regex patterns: `r'(\d+(?:,\d+)*(?:\.\d+)?)\s*([A-Z]{2,10})'` for "100 BTC" format
- Returns `None` for unknown tokens - always check before using price

### 8. Giveaway Rule Parsing (`giveaway_parser.py`)
- Rules extracted via regex patterns, not hardcoded strings
- Four action types: follow, retweet, like, comment (returned as Dict[str, bool])
- Multiple regex patterns per action to catch variations (e.g., "RT", "retweet", "share")
- Comment generation uses random selection from predefined templates - avoid AI generation for simplicity
- `should_participate()` combines price checks, follower counts, and giveaway indicators

### 9. Winner Detection (`winner_detector.py`)
- Mentions-based detection is active (checks last 24h of mentions)
- DM detection requires elevated Twitter API access (placeholder implementation)
- Winner keywords: "congratulations", "winner", "you won", etc.
- Links notifications to giveaways by matching `author_id` and `participated=True`
- Updates both `Giveaway.won` and `Account.total_wins` when winner detected

## Development Workflows

### Adding a New Token
1. Edit `price_checker.py` → `symbol_map` dictionary
2. Add mapping: `'SYMBOL': 'coingecko-id'`
3. Test with `pc = PriceChecker(); print(pc.get_token_price('SYMBOL'))`

### Modifying Search Queries
1. Edit `bot.py` → `_build_search_queries()` method
2. Use Twitter search syntax: `-is:retweet` (exclude), `lang:en` (language), `OR` (alternatives)
3. Keep queries specific to avoid noise - focus on crypto/giveaway keywords

### Adding Comment Templates
1. Edit `giveaway_parser.py` → `generate_comment()` method
2. Add to `comments` list - use emojis and crypto slang for authenticity
3. Keep comments generic to work across different giveaway types

### Testing Without Twitter API
- Use `examples.py` to test individual components
- Mock `tweepy.Client` methods for unit tests
- Query database directly: `sqlite3 giveaways.db`

### Running the Bot
- Development: `python main.py` (runs in foreground with console output)
- Production: Use `screen` or systemd service (see QUICKSTART.md for setup)
- Monitor: `tail -f bot.log` for real-time logs, `python stats.py` for statistics

## Common Pitfalls to Avoid

1. **Don't create new accounts dynamically** - all accounts must be pre-configured in `.env`
2. **Don't bypass rate limiting** - removing delays causes API bans
3. **Don't commit `.env` files** - always use `.env.example` as template
4. **Don't use async/await** - codebase is synchronous, uses `schedule` for periodic tasks
5. **Don't modify SQLAlchemy imports** - use `from sqlalchemy.orm import declarative_base` (not `declarative_base()`)
6. **Don't skip duplicate checks** - always query before inserting `Giveaway` or `WinnerNotification`
7. **Don't use personal Twitter accounts** - bot actions may violate ToS if not properly disclosed

## File Organization

```
bot.py              → Main orchestrator (search → participate → check winners)
main.py             → Entry point with scheduling loop
account_manager.py  → Multi-account management (follow/RT/like/reply methods)
price_checker.py    → CoinGecko integration + token extraction
giveaway_parser.py  → Rule parsing + comment generation
winner_detector.py  → Mention/DM monitoring for wins
models.py           → SQLAlchemy models (Giveaway, Account, WinnerNotification)
config.py           → Environment variable loading + constants
stats.py            → CLI statistics dashboard
setup_verify.py     → Credential verification utility
```

## Integration Points

- **Twitter API v2**: Search via bearer token, actions via OAuth 1.0a user context
- **CoinGecko API**: Free tier for price data (rate limited to ~50 calls/min)
- **SQLite**: Default database (can switch to PostgreSQL via `DATABASE_URL`)
- **Schedule library**: Cron-like periodic task execution in main loop

## Extending the Bot

### Add New Price Source
Extend `PriceChecker._get_price_from_coingecko()` - add fallback methods like `_get_price_from_custom_api()`

### Add Telegram Notifications
Create new module, call from `winner_detector._save_winner_notification()`

### Add Web Dashboard
Create Flask/FastAPI app, query database models for stats, expose REST endpoints

### Improve Winner Detection
Implement `_check_dms()` fully once elevated API access granted - use `client.get_direct_messages()`

---

**Key Insight**: This bot prioritizes reliability over complexity. Rate limiting, error handling, and simple patterns ensure 24/7 operation. When modifying, preserve these safeguards even if refactoring for efficiency.
