# Quick Start Guide

This guide will help you get the Twitter Giveaway Bot up and running quickly.

## Prerequisites

- Python 3.8+ installed
- Git installed
- A Twitter Developer Account
- Multiple Twitter accounts for participation

## Step-by-Step Setup

### 1. Clone and Install

```bash
# Clone the repository
git clone https://github.com/benihutapea/twitterga.git
cd twitterga

# Install dependencies
pip install -r requirements.txt
```

### 2. Get Twitter API Credentials

#### Create Twitter Developer Account

1. Go to https://developer.twitter.com/
2. Sign in with your Twitter account
3. Apply for a developer account
4. Select "Hobbyist" → "Exploring the API"
5. Fill out the application
6. Wait for approval (usually instant to a few hours)

#### Create an App

1. Go to https://developer.twitter.com/en/portal/dashboard
2. Click "Create App"
3. Name your app (e.g., "Giveaway Bot")
4. Save the API keys shown (you'll need these!)

#### Apply for Elevated Access

1. In the Developer Portal, click your app
2. Click "Elevated" under "Access Level"
3. Apply for Elevated Access
4. This is needed for better rate limits

#### Get Credentials for Each Account

For each Twitter account you want to use:

1. Log into that Twitter account
2. Create a new Twitter app for it (or use the same one)
3. Generate:
   - API Key
   - API Key Secret
   - Access Token
   - Access Token Secret
4. Save these credentials

### 3. Configure the Bot

```bash
# Copy the example configuration
cp .env.example .env

# Edit the configuration file
nano .env  # or use your favorite editor
```

Add your credentials:

```bash
# Bearer token from your main app
TWITTER_BEARER_TOKEN=your_actual_bearer_token

# Account 1 credentials
TWITTER_API_KEY_1=your_api_key_here
TWITTER_API_SECRET_1=your_api_secret_here
TWITTER_ACCESS_TOKEN_1=your_access_token_here
TWITTER_ACCESS_SECRET_1=your_access_secret_here

# Account 2 credentials
TWITTER_API_KEY_2=...
TWITTER_API_SECRET_2=...
TWITTER_ACCESS_TOKEN_2=...
TWITTER_ACCESS_SECRET_2=...

# Add more accounts as needed (up to 100)
```

### 4. Verify Setup

```bash
python setup_verify.py
```

This will check:
- ✅ All dependencies are installed
- ✅ Configuration file exists
- ✅ API credentials are valid
- ✅ Accounts can authenticate
- ✅ Database can be initialized

### 5. Run the Bot

```bash
python main.py
```

The bot will:
1. Load all configured accounts
2. Start searching for giveaways
3. Participate in qualifying giveaways
4. Monitor for winner announcements
5. Log everything to `bot.log`

## Understanding the Configuration

### Essential Settings

```bash
# Only participate in tokens worth at least $0.01
MIN_TOKEN_PRICE_USD=0.01

# Use up to 100 accounts per giveaway
MAX_ACCOUNTS_TO_USE=100

# Check for new giveaways every 15 minutes
CHECK_INTERVAL_MINUTES=15

# Only participate if organizer has 1000+ followers
MIN_FOLLOWERS_REQUIRED=1000

# Only participate if estimated value is $50+
MIN_GIVEAWAY_VALUE_USD=50
```

### Adjusting for Your Setup

**If you have few accounts (1-10):**
```bash
MAX_ACCOUNTS_TO_USE=10
CHECK_INTERVAL_MINUTES=30  # Be more conservative
```

**If you have many accounts (50-100):**
```bash
MAX_ACCOUNTS_TO_USE=100
CHECK_INTERVAL_MINUTES=10  # Check more frequently
```

**If you want to be very selective:**
```bash
MIN_TOKEN_PRICE_USD=0.10
MIN_GIVEAWAY_VALUE_USD=100
MIN_FOLLOWERS_REQUIRED=5000
```

**If you want to catch everything:**
```bash
MIN_TOKEN_PRICE_USD=0.001
MIN_GIVEAWAY_VALUE_USD=10
MIN_FOLLOWERS_REQUIRED=500
```

## Monitoring the Bot

### Check Real-time Logs

```bash
tail -f bot.log
```

### View Statistics

```bash
python stats.py
```

This shows:
- Total giveaways found
- Participation rate
- Win count and rate
- Top performing accounts
- Recent activity

### Check Database

```bash
sqlite3 giveaways.db
```

```sql
-- View all giveaways
SELECT * FROM giveaways ORDER BY created_at DESC LIMIT 10;

-- View wins
SELECT * FROM giveaways WHERE won = 1;

-- View account stats
SELECT * FROM accounts ORDER BY total_wins DESC;
```

## Running 24/7

### Option 1: Screen (Simplest)

```bash
# Start a screen session
screen -S twitterbot

# Run the bot
python main.py

# Detach: Press Ctrl+A then D
# Reattach: screen -r twitterbot
```

### Option 2: Systemd (Linux)

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
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable twitterbot
sudo systemctl start twitterbot
sudo systemctl status twitterbot

# View logs
sudo journalctl -u twitterbot -f
```

### Option 3: Docker (Advanced)

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t twitterbot .
docker run -d --name twitterbot \
  -v $(pwd)/.env:/app/.env \
  -v $(pwd)/giveaways.db:/app/giveaways.db \
  twitterbot

# View logs
docker logs -f twitterbot
```

## Troubleshooting

### "Rate limit exceeded"
- Wait 15 minutes and try again
- Increase `CHECK_INTERVAL_MINUTES`
- The bot should handle this automatically

### "Invalid authentication"
- Double-check your API keys in `.env`
- Make sure there are no extra spaces
- Verify the account hasn't been suspended

### "No giveaways found"
- This is normal if there are no current giveaways
- Try lowering `MIN_TOKEN_PRICE_USD`
- Check Twitter manually to see if giveaways exist

### Bot stops unexpectedly
- Check `bot.log` for errors
- Verify API credentials are still valid
- Ensure database isn't corrupted

## Best Practices

### API Usage
- Don't set `CHECK_INTERVAL_MINUTES` below 10
- Don't use more than 100 accounts per giveaway
- Monitor rate limits in logs

### Account Safety
- Use accounts in compliance with Twitter TOS
- Don't use your personal accounts
- Rotate account usage over time
- Monitor for suspicious activity

### Optimization
- Start with conservative settings
- Gradually increase activity
- Monitor win rates
- Adjust thresholds based on results

## Getting Help

1. Check `bot.log` for error messages
2. Run `python setup_verify.py` to diagnose issues
3. Review the full README.md
4. Check existing GitHub issues
5. Open a new issue with:
   - Error message
   - Relevant log entries
   - Your configuration (without credentials!)

## Next Steps

Once your bot is running:

1. **Monitor Performance**
   - Check `stats.py` daily
   - Review win rates
   - Optimize settings

2. **Scale Up**
   - Add more accounts
   - Adjust filters
   - Fine-tune participation

3. **Customize**
   - Edit search queries in `bot.py`
   - Customize comments in `giveaway_parser.py`
   - Add custom filters

4. **Stay Updated**
   - Watch for GitHub updates
   - Check for new features
   - Update dependencies regularly

---

**You're all set! Happy giveaway hunting! 🎉**
