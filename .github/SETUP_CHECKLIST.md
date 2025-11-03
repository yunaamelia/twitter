# Quick Setup Checklist

## ✅ Immediate Actions (5 minutes)

### 1. GitHub Actions Permissions

- [ ] Go to `Settings → Actions → General`
- [ ] Set "Workflow permissions" to **Read and write permissions**
- [ ] Enable "Allow GitHub Actions to create and approve pull requests"

### 2. Enable Dependabot

- [ ] Go to `Settings → Security → Code security and analysis`
- [ ] Enable **Dependency graph**
- [ ] Enable **Dependabot alerts**
- [ ] Enable **Dependabot security updates**

### 3. Install Pre-commit Hooks (Local)

```bash
source .venv/bin/activate
pip install pre-commit
pre-commit install
```

---

## 🔧 Optional Setup (15 minutes)

### 4. Branch Protection (Recommended)

- [ ] Go to `Settings → Branches → Add rule`
- [ ] Branch pattern: `main`
- [ ] Enable: ✅ Require pull request before merging
- [ ] Enable: ✅ Require status checks (select: `test`, `security-check`)

### 5. Codecov Integration (Optional)

- [ ] Visit: https://codecov.io/
- [ ] Login with GitHub
- [ ] Add repository: `benihutapea/twitterga`
- [ ] Copy token
- [ ] Add to GitHub Secrets as `CODECOV_TOKEN`

---

## 🧪 Test Workflows

```bash
# Create test branch
git checkout -b test-workflows
git push origin test-workflows

# Create a PR and watch workflows run
# Check: Repository → Actions tab
```

---

## 📊 Add Badges to README

```markdown
![CI](https://github.com/benihutapea/twitterga/workflows/CI%20-%20Testing%20&%20Quality%20Checks/badge.svg)
![Code Review](https://github.com/benihutapea/twitterga/workflows/Code%20Review/badge.svg)
```

---

## ✨ Done!

All workflows are now configured and ready to use.
