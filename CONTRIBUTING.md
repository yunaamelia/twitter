# Contributing to Twitter Giveaway Bot

Thank you for your interest in contributing to the Twitter Giveaway Bot! This document provides guidelines and instructions for contributing.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [How to Contribute](#how-to-contribute)
5. [Coding Standards](#coding-standards)
6. [Testing Guidelines](#testing-guidelines)
7. [Pull Request Process](#pull-request-process)
8. [Community](#community)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment. We expect:

- Respectful communication
- Constructive feedback
- Focus on what is best for the community
- Empathy towards other community members

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/twitterga.git
   cd twitterga
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/benihutapea/twitterga.git
   ```

## Development Setup

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up configuration**:
   ```bash
   cp .env.example .env
   # Edit .env with your test credentials
   ```

4. **Verify setup**:
   ```bash
   python setup_verify.py
   ```

## How to Contribute

### Reporting Bugs

Before creating a bug report:
- Check if the bug has already been reported in [Issues](https://github.com/benihutapea/twitterga/issues)
- Try the latest version to see if the bug still exists

When creating a bug report, include:
- Clear, descriptive title
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Environment details (OS, Python version, etc.)
- Relevant log excerpts from `bot.log`

### Suggesting Enhancements

Enhancement suggestions are welcome! Include:
- Clear description of the enhancement
- Use cases and benefits
- Possible implementation approach
- Any potential drawbacks

### Contributing Code

1. **Pick an issue** or create one describing what you want to work on
2. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following our coding standards
4. **Test your changes** thoroughly
5. **Commit your changes**:
   ```bash
   git commit -m "Add feature: description"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request** on GitHub

## Coding Standards

### Python Style Guide

Follow PEP 8 guidelines:
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use descriptive variable names
- Add docstrings to all functions and classes

### Code Structure

```python
"""
Module docstring explaining purpose
"""
import standard_library
import third_party_library

from local_module import something

# Constants
CONSTANT_NAME = "value"


class ClassName:
    """Class docstring"""
    
    def method_name(self, param: type) -> return_type:
        """
        Method docstring
        
        Args:
            param: Description
            
        Returns:
            Description
        """
        pass
```

### Documentation

- Add docstrings to all public functions and classes
- Update README.md for user-facing changes
- Update API_DOCS.md for API changes
- Include inline comments for complex logic

### Logging

Use appropriate log levels:
```python
logger.debug("Detailed information for debugging")
logger.info("Normal operation information")
logger.warning("Warning about potential issues")
logger.error("Error that needs attention")
```

## Testing Guidelines

### Manual Testing

1. **Test basic functionality**:
   ```bash
   python examples.py
   ```

2. **Test setup verification**:
   ```bash
   python setup_verify.py
   ```

3. **Test statistics**:
   ```bash
   python stats.py
   ```

### Integration Testing

When adding new features:
1. Test with actual Twitter API (use test accounts)
2. Verify database operations
3. Check rate limiting behavior
4. Test error handling

### Testing Checklist

- [ ] Code runs without errors
- [ ] All imports work correctly
- [ ] Configuration is properly handled
- [ ] Database operations work
- [ ] API calls are properly authenticated
- [ ] Rate limiting is respected
- [ ] Error handling is robust
- [ ] Logging is appropriate

## Pull Request Process

### Before Submitting

1. **Update documentation** if needed
2. **Test your changes** thoroughly
3. **Check code style**:
   ```bash
   # Use a linter if available
   pylint your_file.py
   ```
4. **Sync with upstream**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
Describe how you tested your changes

## Checklist
- [ ] My code follows the project's coding standards
- [ ] I have added docstrings to new functions/classes
- [ ] I have updated documentation as needed
- [ ] I have tested my changes
- [ ] My changes don't break existing functionality
```

### Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, your PR will be merged

## Areas for Contribution

### High Priority

- **Improved winner detection** (DM monitoring with full API access)
- **Web dashboard** for monitoring and control
- **Better token price verification** (multiple sources)
- **Advanced filtering** (ML-based legitimacy scoring)
- **Notification system** (Telegram, Discord, Email)

### Medium Priority

- **Performance optimization** (caching, async operations)
- **Better error handling** (retry logic, fallbacks)
- **Enhanced logging** (structured logging, log rotation)
- **Documentation improvements** (tutorials, videos)
- **Testing infrastructure** (unit tests, integration tests)

### Good First Issues

- **Additional token mappings** in price_checker.py
- **More comment templates** in giveaway_parser.py
- **Documentation typos and clarifications**
- **Configuration validation improvements**
- **Additional example scripts**

## Code Review Guidelines

When reviewing PRs:

### Focus On

- Code correctness and quality
- Performance implications
- Security considerations
- Documentation completeness
- Test coverage

### Be Constructive

- Explain the reasoning behind suggestions
- Offer alternatives when possible
- Acknowledge good work
- Ask questions rather than making demands

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Pull Requests**: Code contributions and reviews

### Getting Help

If you need help:
1. Check existing documentation (README, QUICKSTART, API_DOCS)
2. Search closed issues
3. Ask in GitHub Discussions
4. Create a new issue with the "question" label

## Recognition

Contributors will be:
- Listed in commit history
- Mentioned in release notes for significant contributions
- Added to CONTRIBUTORS.md (if created)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

If you have questions about contributing, feel free to:
- Open an issue with the "question" label
- Ask in GitHub Discussions

Thank you for contributing to Twitter Giveaway Bot! 🎉
