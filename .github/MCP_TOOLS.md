# MCP Tools Configuration for Twitter Bot

## Enabled MCP Servers & Tools

### 1. SQLite Server (Primary Database Operations)

**Server**: `@modelcontextprotocol/server-sqlite`
**Database**: `giveaways.db`

**Available Tools**:

- `read_query` - Execute SELECT queries on giveaways database
- `list_tables` - List all tables (Giveaway, Account, WinnerNotification)
- `describe_table` - Get schema for specific table

**Use Cases**:

- Query giveaway statistics
- Check account participation history
- Analyze winner notifications
- Monitor database health

**Example Queries**:

```sql
-- Get total giveaways by status
SELECT participated, COUNT(*) as count FROM Giveaway GROUP BY participated;

-- Top performing accounts
SELECT account_number, total_participations, total_wins
FROM Account ORDER BY total_wins DESC LIMIT 10;

-- Recent winner notifications
SELECT * FROM WinnerNotification ORDER BY detected_at DESC LIMIT 20;

-- Giveaway conversion rate
SELECT
  COUNT(*) as total,
  SUM(CASE WHEN participated THEN 1 ELSE 0 END) as participated,
  SUM(CASE WHEN won THEN 1 ELSE 0 END) as won
FROM Giveaway;
```

### 2. Filesystem Server (Code & Log Operations)

**Server**: `@modelcontextprotocol/server-filesystem`
**Root**: Workspace folder

**Available Tools**:

- `read_file` - Read Python source files, configs, logs
- `list_directory` - List workspace contents
- `search_files` - Search for specific patterns

**Use Cases**:

- Read bot.log for debugging
- Analyze Python source code
- Check configuration files (.env pattern)
- Monitor file changes

**Key Files to Access**:

- `bot.log` - Bot activity logs
- `config.py` - Configuration management
- `models.py` - Database models
- `account_manager.py` - Multi-account operations
- `price_checker.py` - Token price verification
- `giveaway_parser.py` - Rule parsing
- `winner_detector.py` - Win detection

### 3. GitHub Server (Repository Operations)

**Server**: `@modelcontextprotocol/server-github`
**Repository**: `yunaamelia/twitter`

**Available Tools**:

- `get_file_contents` - Fetch file contents from GitHub
- `search_repositories` - Search GitHub repos
- `create_or_update_file` - Update files remotely
- `push_files` - Multi-file commits
- `create_issue` - Create bug reports/feature requests
- `create_pull_request` - Submit PRs

**Use Cases**:

- Sync code changes to GitHub
- Create issues for bot errors
- Submit automated fixes via PR
- Review workflow status

### 4. Python Server (Code Execution)

**Server**: `@modelcontextprotocol/server-python`

**Available Tools**:

- `execute_code` - Run Python snippets for testing
- `list_packages` - Check installed packages
- `get_package_info` - Get package versions

**Use Cases**:

- Test price_checker logic
- Validate giveaway_parser regex
- Debug account_manager methods
- Quick calculations and data transformations

**Example Executions**:

```python
# Test token price extraction
from price_checker import PriceChecker
pc = PriceChecker()
print(pc.extract_token_value("Win 100 BTC!"))

# Parse giveaway rules
from giveaway_parser import GiveawayParser
gp = GiveawayParser()
rules = gp.parse_giveaway_rules("Follow @user, RT, and like!")
print(rules)

# Check account stats
from models import SessionLocal, Account
db = SessionLocal()
accounts = db.query(Account).all()
for acc in accounts:
    print(f"Account {acc.account_number}: {acc.total_participations} participations, {acc.total_wins} wins")
db.close()
```

### 5. Git Server (Version Control)

**Server**: `@modelcontextprotocol/server-git`
**Repository**: Workspace folder

**Available Tools**:

- `git_status` - Check working tree status
- `git_diff` - View uncommitted changes
- `git_log` - View commit history
- `git_commit` - Commit changes

**Use Cases**:

- Track code modifications
- Review changes before push
- Monitor commit history
- Automate commits

### 6. Memory Server (Persistent Context)

**Server**: `@modelcontextprotocol/server-memory`

**Available Tools**:

- `store_memory` - Save important context
- `retrieve_memory` - Recall stored information
- `search_memory` - Query memory store

**Use Cases**:

- Remember bot performance patterns
- Track recurring issues
- Store optimization notes
- Maintain debugging context across sessions

**What to Store**:

- Rate limit patterns
- Successful giveaway patterns
- Token symbols frequently encountered
- Account performance insights

### 7. Fetch Server (HTTP Requests)

**Server**: `@modelcontextprotocol/server-fetch`

**Available Tools**:

- `fetch` - Make HTTP requests

**Use Cases**:

- Test CoinGecko API manually
- Verify Twitter API endpoints
- Check external services
- Monitor API health

**Example Fetches**:

```
# CoinGecko price check
https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd

# CoinGecko coin search
https://api.coingecko.com/api/v3/search?query=ethereum

# GitHub API rate limits
https://api.github.com/rate_limit
```

## Tool Permissions (alwaysAllow)

All tools have pre-approved operations to streamline workflows:

- **SQLite**: Read-only queries (safe database access)
- **Filesystem**: Read-only operations (no destructive changes)
- **GitHub**: Full CRUD (repository management)
- **Python**: Code execution (testing and validation)
- **Git**: Full operations (version control)
- **Memory**: Full CRUD (context management)
- **Fetch**: HTTP GET requests (API monitoring)

## Integration with Bot Operations

### Scenario 1: Debug Why Bot Isn't Participating

```
1. SQLite: Query recent giveaways with participated=False
2. Filesystem: Read bot.log for error messages
3. Python: Test price_checker.should_participate() logic
4. Memory: Store failure patterns for future reference
```

### Scenario 2: Optimize Giveaway Detection

```
1. SQLite: Analyze which keywords lead to wins
2. Python: Test new regex patterns in giveaway_parser
3. Git: Commit improved patterns
4. GitHub: Push changes and create PR
```

### Scenario 3: Monitor Bot Performance

```
1. SQLite: Query participation/win rates
2. Filesystem: Tail bot.log for real-time activity
3. Memory: Store performance benchmarks
4. Fetch: Check CoinGecko API status
```

### Scenario 4: Fix Critical Bug

```
1. Git: Check git_diff for recent changes
2. Filesystem: Read affected source file
3. Python: Test fix with execute_code
4. SQLite: Verify fix didn't corrupt database
5. GitHub: Create issue documenting bug
6. Git: Commit fix with descriptive message
7. GitHub: Push and close issue
```

## Environment Variables Required

For full MCP functionality, ensure these are set:

```bash
# GitHub MCP Server
export GITHUB_TOKEN="your_github_token_here"

# Twitter Bot (accessed via filesystem/python servers)
export TWITTER_BEARER_TOKEN="your_bearer_token"
export TWITTER_API_KEY_1="your_api_key"
export TWITTER_API_SECRET_1="your_api_secret"
export TWITTER_ACCESS_TOKEN_1="your_access_token"
export TWITTER_ACCESS_SECRET_1="your_access_secret"

# CoinGecko (optional, uses free tier by default)
export COINGECKO_API_KEY="your_coingecko_key"
```

## Security Considerations

1. **SQLite Server**: Read-only queries prevent accidental data corruption
2. **Filesystem Server**: Limited to workspace folder, can't access system files
3. **GitHub Server**: Uses personal access token with repo scope only
4. **Python Server**: Executes in isolated environment
5. **Git Server**: Local repository operations only
6. **Memory Server**: Stores data locally, not shared
7. **Fetch Server**: Only allows GET requests by default

## Disabled Servers (Not Needed)

- **Context7/Upstash**: Already have filesystem access
- **Browser/Playwright**: Bot doesn't need browser automation

## Installation

MCP servers are installed automatically via `npx -y` when Copilot starts. No manual installation required.

## Verification

To verify MCP tools are working:

```bash
# Check installed MCP servers
ls ~/.config/Code\ -\ Insiders/User/mcp/

# Expected servers:
# - modelcontextprotocol.server-sqlite-*
# - modelcontextprotocol.server-filesystem-*
# - modelcontextprotocol.server-github-*
# - modelcontextprotocol.server-python-*
# - modelcontextprotocol.server-git-*
# - modelcontextprotocol.server-memory-*
# - modelcontextprotocol.server-fetch-*
```

## Usage with GitHub Copilot

When chatting with Copilot, you can now:

- Ask database queries: "Show me top 10 accounts by wins"
- Request file analysis: "Read bot.log and find errors"
- Test code: "Execute price_checker with test input"
- Check git status: "What files have uncommitted changes?"
- Store context: "Remember that rate limits occur every 15 minutes"
- Fetch API data: "Check CoinGecko API for Bitcoin price"

Copilot will automatically use the appropriate MCP tool to answer your questions.

## Troubleshooting

**MCP server not responding**:

- Restart VS Code Insiders
- Check `~/.config/Code - Insiders/logs/` for errors
- Verify environment variables are set

**SQLite queries failing**:

- Ensure giveaways.db exists in workspace root
- Check database permissions: `ls -l giveaways.db`

**GitHub operations failing**:

- Verify GITHUB_TOKEN is valid: `gh auth status`
- Check token permissions include `repo` scope

**Python code execution errors**:

- Ensure Python environment is activated
- Install required packages: `pip install -r requirements.txt`

---

**Last Updated**: $(date +%Y-%m-%d)
**Configuration File**: `.github/copilot-mcp.json`
