# MCP Server Configuration

## Active Servers

### SQLite (Active)

**Status:** ✅ Enabled  
**Purpose:** Database query and management for `giveaways.db`  
**Tools:** Query, insert, update, delete database operations  
**Why Enabled:** Essential for viewing and managing bot's database

## Disabled Servers (Can be enabled when needed)

### GitHub (Disabled)

**Status:** ⏸️ Disabled by default  
**Purpose:** GitHub repository management  
**Tools:** Create PRs, manage issues, search code  
**Enable when:** Working on GitHub operations or CI/CD  
**To enable:** Set `"disabled": false` in copilot-mcp.json

### Filesystem (Disabled)

**Status:** ⏸️ Disabled by default  
**Purpose:** Advanced file operations  
**Tools:** File read/write, directory management  
**Enable when:** Need advanced file operations beyond VS Code built-in  
**To enable:** Set `"disabled": false` in copilot-mcp.json  
**Note:** VS Code already has excellent file management built-in

### Context7 (Disabled)

**Status:** ⏸️ Disabled by default  
**Purpose:** Documentation lookup for libraries  
**Tools:** Fetch library docs, API references  
**Enable when:** Need to lookup external library documentation  
**To enable:** Set `"disabled": false` in copilot-mcp.json

### Browser (Disabled)

**Status:** ⏸️ Disabled by default  
**Purpose:** Web automation with Playwright  
**Tools:** Browser automation, web scraping  
**Enable when:** Testing Twitter web interface or automation  
**To enable:** Set `"disabled": false` in copilot-mcp.json

## Why This Configuration?

### Performance Optimization

- **Fewer tools loaded = Faster Copilot response**
- **Reduced memory usage**
- **Less context confusion for AI**

### SQLite is Essential

- Bot uses SQLite database extensively
- Need to query giveaways, accounts, winner notifications
- Quick database inspection during development

### Others are Optional

- **GitHub**: Built-in VS Code Git is sufficient for most tasks
- **Filesystem**: VS Code Explorer handles file operations well
- **Context7**: Can use web browser for documentation
- **Browser**: Only needed for specific web automation tasks

## How to Enable Additional Servers

Edit `.github/copilot-mcp.json`:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["..."],
      "disabled": false // Change to false to enable
    }
  }
}
```

Then reload VS Code: `Ctrl+Shift+P` → "Developer: Reload Window"

## Quick Enable Commands

### Enable GitHub Server

```json
"github": {
  "disabled": false
}
```

### Enable All Servers

```json
{
  "sqlite": { "disabled": false },
  "github": { "disabled": false },
  "filesystem": { "disabled": false },
  "context7": { "disabled": false },
  "browser": { "disabled": false }
}
```

## Performance Impact

| Server     | Tools Count | Memory Usage | Load Time |
| ---------- | ----------- | ------------ | --------- |
| SQLite     | ~10         | Low          | Fast      |
| GitHub     | ~50         | Medium       | Medium    |
| Filesystem | ~20         | Low          | Fast      |
| Context7   | ~5          | Low          | Fast      |
| Browser    | ~30         | High         | Slow      |

**Current Config:** Only SQLite = ~10 tools loaded (optimized!)

## Recommended Usage

### Daily Development

- ✅ SQLite only (current config)
- Fast and focused on database operations

### When Working with GitHub

- ✅ SQLite + GitHub
- For PR management and code search

### Advanced Debugging

- ✅ SQLite + Browser
- For testing Twitter web interactions

### Full Power Mode

- ✅ All servers enabled
- When you need all capabilities (slower but complete)

---

**Current Status: Optimized for Performance** 🚀

Only SQLite is active to keep Copilot fast and responsive!
