# Quick Reference Card

## Essential Commands

### Running the Bot

```bash
make run              # Run with Makefile
python main.py        # Run directly
python dev.py run     # Run with dev script
F5                    # Debug in VS Code
```

### Development

```bash
make format          # Format code (Black + isort)
make lint            # Lint code (Pylint + Flake8)
make test            # Run tests
make clean           # Clean cache files
```

### Monitoring

```bash
make stats           # Show statistics
make logs            # Tail logs
python stats.py      # Direct stats
tail -f bot.log      # Direct logs
```

### Database

```bash
make db-shell        # Open SQLite shell
make db-query        # Quick query
sqlite3 giveaways.db # Direct access
```

## VS Code Shortcuts

### Debug

- `F5` - Start Debugging
- `Shift+F5` - Stop Debugging
- `F9` - Toggle Breakpoint
- `F10` - Step Over
- `F11` - Step Into

### Code

- `Shift+Alt+F` - Format Document
- `Ctrl+.` - Quick Fix
- `F12` - Go to Definition
- `Shift+F12` - Find References
- `Ctrl+/` - Toggle Comment

### Navigation

- `Ctrl+P` - Quick Open File
- `Ctrl+Shift+O` - Go to Symbol
- `Ctrl+G` - Go to Line
- `Ctrl+Tab` - Switch Editor
- `Ctrl+B` - Toggle Sidebar

### Terminal

- `` Ctrl+`  `` - Toggle Terminal
- `Ctrl+Shift+` ` - New Terminal
- `Ctrl+Shift+5` - Split Terminal

### GitHub Copilot

- `Ctrl+I` - Copilot Chat
- `Alt+\` - Toggle Suggestions
- `Tab` - Accept Suggestion
- `Alt+]` - Next Suggestion

## Code Snippets

Type prefix + Tab:

| Prefix        | Description             |
| ------------- | ----------------------- |
| `tw-client`   | Twitter API client      |
| `db-session`  | Database session        |
| `log-setup`   | Logger setup            |
| `try-log`     | Try-except with logging |
| `tw-search`   | Twitter search query    |
| `rate-limit`  | Rate limiting delay     |
| `cfg-account` | Get account credentials |
| `parse-rules` | Giveaway rules dict     |
| `cg-price`    | CoinGecko price check   |
| `doc-func`    | Function docstring      |

## File Structure

```
twitterga/
├── bot.py              # Main orchestrator
├── main.py             # Entry point
├── account_manager.py  # Multi-account handler
├── price_checker.py    # Token price verification
├── giveaway_parser.py  # Rule extraction
├── winner_detector.py  # Winner monitoring
├── models.py           # Database models
├── config.py           # Configuration
├── stats.py            # Statistics
└── setup_verify.py     # Setup verification
```

## Common Tasks

### Add New Token

1. Edit `price_checker.py`
2. Add to `symbol_map` dict
3. Test: `pc.get_token_price('SYMBOL')`

### Modify Search

1. Edit `bot.py` → `_build_search_queries()`
2. Use Twitter syntax: `-is:retweet lang:en`
3. Test with single cycle

### Add Comment Template

1. Edit `giveaway_parser.py` → `generate_comment()`
2. Add to `comments` list
3. Keep generic and emoji-friendly

### Debug Issue

1. Set breakpoint (F9)
2. Press F5
3. Inspect variables
4. Step through code (F10/F11)

## Configuration Files

| File                    | Purpose                             |
| ----------------------- | ----------------------------------- |
| `.env`                  | Environment variables & credentials |
| `.vscode/settings.json` | VS Code workspace settings          |
| `.vscode/launch.json`   | Debug configurations                |
| `.vscode/tasks.json`    | Build & run tasks                   |
| `.pylintrc`             | Pylint configuration                |
| `.flake8`               | Flake8 configuration                |
| `pyproject.toml`        | Python project config               |
| `Makefile`              | Development commands                |

## Troubleshooting

### Import Error

```bash
export PYTHONPATH="${PWD}:${PYTHONPATH}"
```

### Python Not Found

```
Ctrl+Shift+P → "Python: Select Interpreter"
Choose: .venv/bin/python
```

### Extension Not Working

```
Ctrl+Shift+P → "Developer: Reload Window"
```

### Database Locked

```bash
# Stop all bot instances
pkill -f main.py
```

### Rate Limited

- Increase `CHECK_INTERVAL_MINUTES` in .env
- Reduce `MAX_ACCOUNTS_TO_USE`
- Wait 15 minutes for reset

## Quick Database Queries

```sql
-- Recent giveaways
SELECT tweet_id, token_symbol, estimated_value_usd, participated
FROM giveaways ORDER BY created_at DESC LIMIT 10;

-- Active accounts
SELECT account_number, username, total_participations, total_wins
FROM accounts WHERE is_active = 1;

-- Recent wins
SELECT * FROM winner_notifications
ORDER BY received_at DESC LIMIT 10;

-- Win rate
SELECT
  COUNT(*) as total,
  SUM(CASE WHEN won = 1 THEN 1 ELSE 0 END) as wins,
  ROUND(100.0 * SUM(CASE WHEN won = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) as win_rate
FROM giveaways WHERE participated = 1;
```

## Environment Variables

Essential variables in `.env`:

```bash
# Twitter API
TWITTER_BEARER_TOKEN=...
TWITTER_API_KEY_1=...
TWITTER_API_SECRET_1=...
TWITTER_ACCESS_TOKEN_1=...
TWITTER_ACCESS_SECRET_1=...

# Bot Settings
MIN_TOKEN_PRICE_USD=0.01
MAX_ACCOUNTS_TO_USE=100
CHECK_INTERVAL_MINUTES=15
MIN_FOLLOWERS_REQUIRED=1000
MIN_GIVEAWAY_VALUE_USD=50
```

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and format
make format

# Commit
git add .
git commit -m "Add: new feature"

# Push
git push origin feature/new-feature
```

## Production Deployment

```bash
# Using screen
screen -S twitterbot
python main.py
# Ctrl+A then D to detach

# Using systemd
sudo systemctl start twitterbot
sudo systemctl status twitterbot
sudo journalctl -u twitterbot -f
```

---

**Keep this handy while developing!** 📌
