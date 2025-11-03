# MCP Tools Setup - Quick Reference

## 🚀 Quick Start

### 1. Set GitHub Token

```bash
echo 'export GITHUB_TOKEN="your_github_token_here"' >> ~/.bashrc
source ~/.bashrc
```

Or for current session only:

```bash
export GITHUB_TOKEN="your_github_token_here"
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create Database (Optional)

```bash
python3 -c "from models import Base, engine; Base.metadata.create_all(engine); print('Database created!')"
```

### 4. Test MCP Tools

```bash
./test_mcp.sh
```

### 5. Start VS Code Insiders

```bash
code-insiders .
```

MCP servers will auto-install on first GitHub Copilot use.

## 🛠️ Available MCP Tools

| Server         | Purpose          | Key Tools                                         |
| -------------- | ---------------- | ------------------------------------------------- |
| **sqlite**     | Database queries | `read_query`, `list_tables`, `describe_table`     |
| **filesystem** | File operations  | `read_file`, `list_directory`, `search_files`     |
| **github**     | Git hosting      | `get_file_contents`, `create_issue`, `push_files` |
| **python**     | Code execution   | `execute_code`, `list_packages`                   |
| **git**        | Version control  | `git_status`, `git_diff`, `git_log`               |
| **memory**     | Context storage  | `store_memory`, `retrieve_memory`                 |
| **fetch**      | HTTP requests    | `fetch`                                           |

## 💬 Example Copilot Prompts

### Database Operations

```
Show me all giveaways participated in the last 24 hours
List top 10 accounts by win rate
Count total winners detected
```

### File Analysis

```
Read bot.log and find rate limit errors
Show me the price_checker.py implementation
List all Python files in the workspace
```

### Code Testing

```
Execute price_checker to extract tokens from "Win 100 BTC"
Test giveaway_parser with sample tweet
Validate config.py settings
```

### Git Operations

```
What files have uncommitted changes?
Show git diff for bot.py
Display last 5 commits
```

### API Monitoring

```
Check CoinGecko API status
Fetch Bitcoin current price
Test Twitter API rate limits
```

## 🔧 Troubleshooting

### MCP Server Not Found

- **Symptom**: Tools not available in Copilot
- **Fix**: Restart VS Code Insiders, servers install on first use

### SQLite Database Error

- **Symptom**: "giveaways.db not found"
- **Fix**: Run bot once to create database, or use creation command above

### GitHub Token Invalid

- **Symptom**: GitHub operations fail
- **Fix**: Verify token with `gh auth status`, regenerate if expired

### Python Packages Missing

- **Symptom**: Import errors in `execute_code`
- **Fix**: Run `pip install -r requirements.txt`

## 📚 Full Documentation

See `.github/MCP_TOOLS.md` for comprehensive documentation including:

- Detailed tool descriptions
- Security considerations
- Integration scenarios
- Advanced usage patterns

## ✅ Verification Checklist

Run `./test_mcp.sh` to check:

- ✓ MCP servers installed
- ✓ Environment variables set
- ✓ Database ready
- ✓ Python packages installed
- ✓ Git repository configured
- ✓ Bot files present
- ✓ CoinGecko API reachable

## 🎯 Common Workflows

### Debug Bot Issue

1. Ask Copilot: "Read bot.log for errors"
2. Ask Copilot: "Query failed giveaways from database"
3. Ask Copilot: "Test price_checker logic"
4. Ask Copilot: "Store debugging notes in memory"

### Optimize Bot Performance

1. Ask Copilot: "Show account participation statistics"
2. Ask Copilot: "Analyze winner patterns in database"
3. Ask Copilot: "Test improved giveaway parser regex"
4. Ask Copilot: "Commit and push optimizations"

### Monitor Bot Health

1. Ask Copilot: "Check database record counts"
2. Ask Copilot: "Tail bot.log for real-time activity"
3. Ask Copilot: "Fetch CoinGecko API health"
4. Ask Copilot: "Show git status"

---

**Last Updated**: 2025-01-27
**Configuration**: `.github/copilot-mcp.json`
**Test Script**: `test_mcp.sh`
