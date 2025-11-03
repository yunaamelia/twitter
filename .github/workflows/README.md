# GitHub Actions Workflows

## Overview

This directory contains GitHub Actions workflows for automated CI/CD, code review, performance monitoring, and dependency management.

## Workflows

### 1. CI - Testing & Quality Checks (`ci.yml`)

**Triggers:** Push to main/develop, Pull Requests

**Features:**

- Multi-version Python testing (3.8, 3.9, 3.10, 3.11)
- Code formatting check with Black
- Import sorting check with isort
- Linting with Flake8 and Pylint
- Unit tests with pytest and coverage reporting
- Security scanning with Safety and Bandit
- Automatic upload to Codecov

### 2. Code Review (`code-review.yml`)

**Triggers:** Pull Requests

**Features:**

- GitHub Copilot automated code review
- Code quality metrics with Radon
- Complexity analysis
- Maintainability index calculation
- Automatic PR comments with quality report

### 3. Performance & Optimization (`performance.yml`)

**Triggers:** Push to main, Pull Requests, Weekly schedule

**Features:**

- Memory profiling
- Code complexity analysis
- Cyclomatic complexity measurement
- Maintainability index
- Code smell detection
- Dependency vulnerability scanning
- Performance report artifacts

### 4. Dependency Updates (`dependency-update.yml`)

**Triggers:** Weekly schedule (Sunday), Manual dispatch

**Features:**

- Automatic dependency updates
- Security vulnerability scanning with pip-audit
- Auto-generated pull requests for updates
- Backup and rollback support

## Required Dependencies

Add these to `requirements-dev.txt` if not already present:

```txt
pytest-cov
safety
bandit
radon
xenon
memory-profiler
py-spy
pip-audit
pip-tools
```

## Setup

1. Ensure all dependencies are installed:

   ```bash
   pip install -r requirements-dev.txt
   ```

2. (Optional) Set up Codecov token in repository secrets:

   - Go to repository Settings → Secrets and variables → Actions
   - Add `CODECOV_TOKEN` secret

3. (Optional) Enable GitHub Copilot review:
   - Ensure GitHub Copilot is enabled for your repository

## Local Testing

Run the same checks locally before pushing:

```bash
# Full quality check
make quality

# Or individual checks
black --check --line-length 100 *.py
isort --check-only *.py
flake8 *.py --max-line-length=100
pylint *.py
pytest -v --cov=.
```

## Workflow Status Badges

Add these to your README.md:

```markdown
![CI](https://github.com/benihutapea/twitterga/workflows/CI%20-%20Testing%20&%20Quality%20Checks/badge.svg)
![Code Review](https://github.com/benihutapea/twitterga/workflows/Code%20Review/badge.svg)
![Performance](https://github.com/benihutapea/twitterga/workflows/Performance%20&%20Optimization/badge.svg)
```
