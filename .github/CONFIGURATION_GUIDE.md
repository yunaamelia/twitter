# GitHub Workflows Configuration Guide

## 📋 Daftar Konfigurasi yang Sudah Ada

### ✅ Workflows

- `ci.yml` - Testing & Quality Checks
- `code-review.yml` - Automated Code Review
- `performance.yml` - Performance & Optimization
- `dependency-update.yml` - Dependency Updates
- `notification.yml` - Workflow Notifications

### ✅ Konfigurasi Linting & Formatting

- `.flake8` - Flake8 configuration
- `.pylintrc` - Pylint configuration
- `pyproject.toml` - Black, isort, pytest, mypy config
- `.pre-commit-config.yaml` - Pre-commit hooks

### ✅ GitHub Templates

- `.github/ISSUE_TEMPLATE/bug_report.yml`
- `.github/ISSUE_TEMPLATE/feature_request.yml`
- `.github/pull_request_template.md`

### ✅ Dependency Management

- `.github/dependabot.yml` - Automated dependency updates
- `.codecov.yml` - Code coverage configuration

---

## 🔧 Konfigurasi yang Masih Perlu Dilakukan

### 1. **GitHub Repository Secrets** (WAJIB!)

Buka: `Settings → Secrets and variables → Actions → New repository secret`

#### Required Secrets:

```bash
# Optional - untuk coverage reporting yang lebih baik
CODECOV_TOKEN=your_codecov_token_here

# Optional - untuk notifikasi Slack
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Optional - untuk notifikasi Discord
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR/WEBHOOK/URL
```

**Cara mendapatkan Codecov Token:**

1. Buka https://codecov.io/
2. Login dengan GitHub account
3. Add repository `benihutapea/twitterga`
4. Copy token dari Settings
5. Tambahkan ke GitHub Secrets

---

### 2. **Branch Protection Rules**

Buka: `Settings → Branches → Add rule`

#### Konfigurasi untuk branch `main`:

**Branch name pattern:** `main`

**Protection rules yang direkomendasikan:**

- ✅ Require a pull request before merging
  - Require approvals: 1
  - Dismiss stale pull request approvals when new commits are pushed
- ✅ Require status checks to pass before merging
  - Require branches to be up to date before merging
  - Status checks yang required:
    - `test (3.10)` (pilih minimal 1 Python version)
    - `security-check`
    - `code-quality-review`
- ✅ Require conversation resolution before merging
- ✅ Require linear history (optional)
- ✅ Include administrators (optional, untuk enforce rules)

---

### 3. **GitHub Actions Permissions**

Buka: `Settings → Actions → General`

**Workflow permissions:**

- ✅ Read and write permissions (untuk auto-commit, PR creation, dll)
- ✅ Allow GitHub Actions to create and approve pull requests

---

### 4. **Enable Dependabot Alerts**

Buka: `Settings → Security → Code security and analysis`

**Enable:**

- ✅ Dependency graph
- ✅ Dependabot alerts
- ✅ Dependabot security updates

---

### 5. **Setup Pre-commit Hooks (Local Development)**

Jalankan di local repository:

```bash
# Aktivasi virtual environment
source .venv/bin/activate

# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install

# (Optional) Run on all files
pre-commit run --all-files
```

**Sekarang setiap git commit akan otomatis:**

- Format code dengan Black
- Sort imports dengan isort
- Run Flake8
- Check YAML/JSON syntax
- Remove trailing whitespace

---

### 6. **Setup GitHub Copilot Review (Optional)**

Untuk mengaktifkan Copilot Review otomatis:

1. Pastikan GitHub Copilot aktif untuk organization/account
2. Workflow sudah dikonfigurasi di `code-review.yml`
3. Tidak perlu konfigurasi tambahan - otomatis akan berjalan pada PR

**Note:** Jika tidak ada akses Copilot, workflow akan skip step ini tanpa error.

---

### 7. **Setup Codecov (Optional)**

Jika ingin coverage reporting:

```bash
# 1. Buka https://codecov.io/
# 2. Login dengan GitHub
# 3. Add repository: benihutapea/twitterga
# 4. Copy token
# 5. Add ke GitHub Secrets sebagai CODECOV_TOKEN
```

**Tambahan untuk README.md:**

```markdown
[![codecov](https://codecov.io/gh/benihutapea/twitterga/branch/main/graph/badge.svg)](https://codecov.io/gh/benihutapea/twitterga)
```

---

## 🚀 Testing Workflows

### Test Locally (sebelum push):

```bash
# Format & lint
make format
make lint

# Run tests
make test

# Verify setup
make verify
```

### Test Workflows di GitHub:

1. **Push ke branch lain:**

   ```bash
   git checkout -b test-workflows
   git push origin test-workflows
   ```

2. **Buat Pull Request:**

   - Workflows akan otomatis berjalan
   - Review hasil di tab "Actions"
   - Check PR comments untuk code quality report

3. **Merge jika semua hijau ✅**

---

## 📊 Monitoring & Maintenance

### Melihat Workflow Status:

```bash
# Melalui GitHub UI
Repository → Actions tab

# Atau gunakan GitHub CLI
gh run list
gh run view <run-id>
```

### Melihat Coverage Reports:

```bash
# Local
pytest --cov=. --cov-report=html
open htmlcov/index.html

# GitHub
Check Codecov dashboard atau PR comments
```

### Update Dependencies:

Dependabot akan otomatis membuat PR setiap minggu.
Review dan merge PR tersebut.

---

## 🛠️ Troubleshooting

### Workflow gagal karena missing dependencies:

**Solution:** Update `requirements-dev.txt` atau cek workflow logs

### Pre-commit hooks gagal:

```bash
# Skip hooks untuk emergency commit
git commit --no-verify -m "emergency fix"

# Atau fix issues yang dilaporkan
black *.py
isort *.py
flake8 *.py
```

### Coverage terlalu rendah:

**Solution:** Tambahkan tests di `tests/` directory

### Workflow terlalu lambat:

**Solution:** Reduce Python version matrix di `ci.yml` (hanya test 1-2 versions)

---

## 📝 Next Steps

1. ✅ Add GitHub Secrets (Codecov token)
2. ✅ Setup Branch Protection Rules
3. ✅ Enable Dependabot
4. ✅ Install pre-commit hooks locally
5. ✅ Test workflows dengan PR
6. ✅ Add badges ke README.md

---

## 🔗 Useful Links

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Codecov Documentation](https://docs.codecov.com/)
- [Pre-commit Documentation](https://pre-commit.com/)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
