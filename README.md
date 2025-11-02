# Twitter Giveaway Bot 🎁🤖

An advanced automated bot designed to find and participate in cryptocurrency giveaways on Twitter. The bot can manage 100+ Twitter accounts simultaneously, automatically detect crypto token giveaways, verify token prices, participate according to giveaway rules, and monitor for winner announcements.

## Features ✨

### 🔍 Intelligent Giveaway Detection
- Automatically searches Twitter for cryptocurrency and token giveaways
- Filters giveaways based on token price verification
- Only participates in giveaways for tokens with real market value
- Configurable minimum price and giveaway value thresholds

### 🤖 Multi-Account Management
- Supports 100+ Twitter accounts simultaneously
- Automatic account rotation and load balancing
- Tracks participation statistics per account
- Rate limiting to avoid API restrictions

### 📋 Rule Parsing & Participation
- Automatically detects giveaway requirements:
  - **Follow** - Follows the organizer's account
  - **Retweet** - Retweets the giveaway post
  - **Like** - Likes the giveaway post
  - **Comment** - Posts engaging comments
- Generates natural, varied comments to avoid spam detection

### 💰 Price Verification
- Integrates with CoinGecko API for real-time token prices
- Only participates in giveaways for tokens with verified market prices
- Configurable minimum token price threshold
- Supports major cryptocurrencies (BTC, ETH, BNB, SOL, ADA, XRP, etc.)

### 🏆 Winner Detection
- Monitors Twitter mentions for winner announcements
- Tracks when accounts are tagged by giveaway organizers
- Support for DM winner notifications (requires elevated API access)
- Automatic win rate tracking and statistics

### 📊 Statistics & Tracking
- Database storage for all giveaways and participations
- Track wins per account
- Monitor participation rates
- Generate performance reports

## Requirements 📋

- Python 3.8 or higher
- Twitter Developer Account with API access
- Multiple Twitter accounts for participation (1-100+)
- CoinGecko API key (optional, for better price data)

## Installation 🔧

1. **Clone the repository:**
```bash
git clone https://github.com/benihutapea/twitterga.git
cd twitterga
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up configuration:**
```bash
cp .env.example .env
```

4. **Edit the `.env` file with your credentials:**
```bash
nano .env
```

## Configuration ⚙️

### Getting Twitter API Credentials

1. **Apply for Twitter Developer Account:**
   - Visit https://developer.twitter.com/en/portal/dashboard
   - Apply for Elevated Access (required for some features)
   - Create a new App in the Developer Portal

2. **Get Bearer Token:**
   - In your app settings, find the Bearer Token
   - Add it to `.env` as `TWITTER_BEARER_TOKEN`

3. **Get API Keys for Each Account:**
   - For each Twitter account you want to use:
     - Generate API Key and Secret
     - Generate Access Token and Secret
     - Add them to `.env` with numbered suffixes:
       ```
       TWITTER_API_KEY_1=your_api_key
       TWITTER_API_SECRET_1=your_api_secret
       TWITTER_ACCESS_TOKEN_1=your_access_token
       TWITTER_ACCESS_SECRET_1=your_access_secret
       ```

### Configuration Options

Edit `.env` to customize bot behavior:

```bash
# Minimum token price (USD) to consider giveaway valuable
MIN_TOKEN_PRICE_USD=0.01

# Maximum number of accounts to use per giveaway
MAX_ACCOUNTS_TO_USE=100

# How often to check for new giveaways (minutes)
CHECK_INTERVAL_MINUTES=15

# Minimum followers required for giveaway organizer
MIN_FOLLOWERS_REQUIRED=1000

# Minimum estimated giveaway value (USD)
MIN_GIVEAWAY_VALUE_USD=50
```

## Usage 🚀

### Basic Usage

Start the bot:
```bash
python main.py
```

The bot will:
1. Initialize all configured accounts
2. Search for crypto giveaways every 15 minutes (configurable)
3. Automatically participate in qualifying giveaways
4. Monitor for winner announcements
5. Log all activities to `bot.log`

### Running as a Background Service

**Linux/Mac (using screen):**
```bash
screen -S twitterbot
python main.py
# Press Ctrl+A then D to detach
```

**Linux (using systemd):**

Create `/etc/systemd/system/twitterbot.service`:
```ini
[Unit]
Description=Twitter Giveaway Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/twitterga
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable twitterbot
sudo systemctl start twitterbot
sudo systemctl status twitterbot
```

## How It Works 🔧

### 1. Giveaway Search
The bot searches Twitter using optimized queries:
- "crypto giveaway"
- "token giveaway"
- "BTC giveaway", "ETH giveaway"
- "crypto airdrop"

### 2. Filtering
Each found tweet is analyzed:
- ✅ Contains giveaway keywords
- ✅ Mentions cryptocurrency/tokens
- ✅ Token has verifiable market price
- ✅ Token price meets minimum threshold
- ✅ Organizer has sufficient followers
- ✅ Estimated value meets minimum

### 3. Rule Parsing
The bot intelligently parses giveaway rules:
```
Example Tweet: "🎁 GIVEAWAY 🎁
Win 100 $TOKEN!
✅ Follow @Organizer
✅ Retweet
✅ Like
✅ Comment your wallet"
```

The bot detects all required actions automatically.

### 4. Participation
For each qualifying giveaway:
- Multiple accounts participate (up to configured limit)
- All required actions are performed
- Rate limiting prevents API restrictions
- Actions are logged to database

### 5. Winner Detection
The bot monitors:
- **Mentions**: Checks if organizer tagged your accounts
- **DMs**: Checks for winner notification messages (requires elevated API)
- Automatically updates win statistics

## Database Schema 📊

The bot uses SQLite by default with three main tables:

### Giveaways
Stores all detected giveaways with:
- Tweet information
- Token details and price
- Participation status
- Winner status

### Accounts
Tracks all managed accounts:
- Account credentials reference
- Usage statistics
- Win tracking

### WinnerNotifications
Logs all winner announcements:
- Notification type (DM/mention)
- Associated giveaway
- Timestamp

## API Rate Limits ⚠️

Twitter API has rate limits:
- **Search**: 180 requests per 15 minutes (per app)
- **User Timeline**: 900 requests per 15 minutes (per account)
- **Follow/Retweet/Like**: Various limits per account

The bot includes:
- Automatic rate limit handling
- Built-in delays between actions
- Request distribution across accounts

## Security & Privacy 🔒

- Never commit `.env` file with credentials
- Use separate API apps for different account groups
- Keep bearer tokens and secrets private
- Monitor accounts for suspicious activity
- Use accounts in compliance with Twitter TOS

## Troubleshooting 🔍

### "Invalid authentication credentials"
- Verify all API keys are correct in `.env`
- Ensure bearer token has proper permissions
- Check that accounts haven't been suspended

### "Rate limit exceeded"
- Increase `CHECK_INTERVAL_MINUTES`
- Reduce `MAX_ACCOUNTS_TO_USE`
- The bot should auto-handle this, but manual adjustment may help

### "No giveaways found"
- Check that search queries return results manually
- Verify `MIN_TOKEN_PRICE_USD` isn't too high
- Try adjusting `MIN_FOLLOWERS_REQUIRED`

### "Database is locked"
- Only run one instance of the bot
- Check file permissions on database file

## Statistics Example 📈

The bot logs comprehensive statistics:

```
📊 Statistics:
  - Total giveaways found: 145
  - Total participations: 89
  - Total wins: 7
  - Active accounts: 50
  - Win rate: 7.87%
```

## Advanced Features 🚀

### Custom Search Queries
Edit `bot.py` to add custom search queries:
```python
def _build_search_queries(self) -> List[str]:
    return [
        "your custom query -is:retweet lang:en",
        # Add more...
    ]
```

### Custom Comment Templates
Edit `giveaway_parser.py` to customize comments:
```python
comments = [
    "Your custom comment!",
    # Add more...
]
```

### Price Source Integration
The bot uses CoinGecko but can be extended to use other price APIs in `price_checker.py`.

## Contributing 🤝

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Disclaimer ⚖️

This bot is for educational purposes. Users are responsible for:
- Complying with Twitter's Terms of Service
- Not engaging in spam or abusive behavior
- Following applicable laws and regulations
- Using the bot ethically and responsibly

The authors are not responsible for:
- Account suspensions or bans
- Loss of funds or opportunities
- Any damages resulting from bot usage

## License 📄

MIT License - See LICENSE file for details

## Support 💬

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review documentation thoroughly

## Roadmap 🗺️

Future enhancements:
- [ ] Web dashboard for monitoring
- [ ] Telegram notifications for wins
- [ ] ML-based giveaway legitimacy scoring
- [ ] Multi-chain token price verification
- [ ] Automatic wallet address submission
- [ ] Discord integration
- [ ] Advanced analytics and reporting

---

**Happy Giveaway Hunting! 🎉🚀**