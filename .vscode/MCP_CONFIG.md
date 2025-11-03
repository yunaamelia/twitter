# MCP Server Configuration

## 🔌 Active MCP Servers

### 1. **GitHub MCP Server** ✅

- **Provider**: `github/github-mcp-server`
- **Version**: 0.13.0
- **Type**: HTTP
- **Purpose**: GitHub repository management, PRs, issues, and workflows
- **Use Cases**:
  - Create and manage pull requests
  - Review code changes
  - Manage issues and labels
  - GitHub Actions workflow management
  - Repository operations

### 2. **Context7 (Upstash)** ✅

- **Provider**: `upstash/context7`
- **Version**: 1.0.0
- **Type**: HTTP
- **Purpose**: Up-to-date library documentation
- **Use Cases**:
  - Tweepy API documentation
  - SQLAlchemy documentation
  - Python library references
  - CoinGecko API docs
  - Any pip package documentation
- **API Key**: Optional (increases rate limits)
  - Get at: https://context7.com/dashboard

### 3. **GitKraken MCP Server** ✅

- **Provider**: `gitkraken/gitkraken-mcp-server`
- **Version**: 1.0.0
- **Type**: HTTP
- **Purpose**: Advanced Git operations
- **Use Cases**:
  - Git branch management
  - Commit operations
  - Git stash operations
  - Pull/Push operations
  - Git history and diffs

### 4. **Pylance MCP Server** (Built-in) ✅

- **Provider**: `ms-python.vscode-pylance`
- **Type**: Built-in extension MCP
- **Purpose**: Python code analysis and intelligence
- **Use Cases**:
  - Python type checking
  - Code refactoring
  - Import management
  - Python environment management

---

## 🗑️ Removed MCP Servers

### ~~Microsoft Playwright MCP~~ ❌

- **Reason**: Not needed for Twitter bot project
- **Why**: Browser automation is not required
- **Alternative**: None needed
- **Removed**: 2025-11-03

---

## 📁 Configuration Files

### User-level Config

```
~/.config/Code - Insiders/User/mcp.json
```

### Project-level Config

```
.vscode/mcp.json (this file for documentation)
```

---

## 🔧 Setup Instructions

### 1. Update User MCP Configuration

Copy the optimized config to your user settings:

```bash
# Backup current config
cp ~/.config/Code\ -\ Insiders/User/mcp.json ~/.config/Code\ -\ Insiders/User/mcp.json.backup

# Apply new config (will be created via script)
```

### 2. Remove Playwright MCP

```bash
# Remove playwright MCP directory
rm -rf ~/.config/Code\ -\ Insiders/User/mcp/microsoft.playwright-mcp-0.0.1-seed
```

### 3. Reload VS Code

Press `Ctrl+Shift+P` → `Developer: Reload Window`

---

## 💡 Usage Examples

### GitHub MCP

```
Ask Copilot:
- "Create a PR for this branch"
- "List open issues in the repo"
- "Show recent pull requests"
- "Request Copilot review on PR #123"
```

### Context7 (Documentation)

```
Ask Copilot:
- "Get Tweepy v2 API documentation"
- "Show SQLAlchemy session management docs"
- "How to use CoinGecko API?"
- "Latest tweepy.Client methods"
```

### GitKraken MCP

```
Ask Copilot:
- "Show git status"
- "Create new branch feature/xyz"
- "Git stash current changes"
- "Show git log for last 10 commits"
```

### Pylance MCP

```
Ask Copilot:
- "Refactor this function"
- "Remove unused imports"
- "Fix all import formatting"
- "Check Python environment"
```

---

## 🚀 Benefits

1. **GitHub Integration**: Seamless PR and issue management
2. **Live Documentation**: Always up-to-date library docs
3. **Git Operations**: Advanced Git workflow support
4. **Python Intelligence**: Built-in Python code analysis

---

## 🔑 API Keys (Optional)

### Context7 API Key

- **Get Key**: https://context7.com/dashboard
- **Benefit**: Higher rate limits for documentation queries
- **Storage**: Stored securely in VS Code settings
- **Required**: No (works without, but with limits)

---

## 📊 Performance Impact

- **Before**: 3 MCP servers (including unused Playwright)
- **After**: 3 essential MCP servers + 1 built-in
- **Reduction**: Removed 1 unnecessary server
- **Startup**: Faster (no Playwright node process)
- **Memory**: Lower (no browser automation overhead)

---

## 🛠️ Troubleshooting

### MCP Server Not Working

1. Check VS Code Output panel
2. Look for MCP server logs in: `~/.config/Code - Insiders/logs/`
3. Reload window: `Ctrl+Shift+P` → `Developer: Reload Window`

### GitHub MCP Issues

- Ensure GitHub Copilot is active
- Check internet connection
- Verify GitHub token in settings

### Context7 Rate Limits

- Sign up for free API key
- Add key via VS Code prompt

---

## ✅ Verification

Run this to verify MCP setup:

```bash
# Check active MCP servers
cat ~/.config/Code\ -\ Insiders/User/mcp.json | jq '.servers | keys'

# Check MCP logs
ls -la ~/.config/Code\ -\ Insiders/logs/*/window*/mcpServer.*
```

Expected output: github, upstash, gitkraken, pylance
