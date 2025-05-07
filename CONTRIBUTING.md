# Contributing to Knowledge Base Builder

Thank you for your interest in contributing to Knowledge Base Builder! This document provides guidelines and instructions for contributing.

## Quick Start

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add your feature'`)
5. Push to the branch (`git push origin feature/your-feature`)
6. Create a Pull Request

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/knowledge-base-builder.git
   cd knowledge-base-builder
   ```

2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

3. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Add tests for new features or bug fixes
3. Ensure all tests pass
4. Update documentation if needed
5. The PR will be merged once you have the sign-off of at least one maintainer

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings for new functions and classes
- Keep functions focused and small
- Write clear commit messages

## Testing

Run tests with:
```bash
pytest
```

## Bug Reports

Found a bug? Here's how to report it:

1. Check if the bug has already been reported in the Issues section
2. If not, create a new issue
3. Include:
   - A clear title
   - Steps to reproduce the bug
   - Expected vs actual behavior
   - Your environment (OS, Python version, etc.)

## Feature Requests

Have an idea for a new feature? Great! Please:

1. Check if the feature has already been requested
2. Create a new issue with the "enhancement" label
3. Describe the feature and its benefits
4. Include any relevant examples or use cases

## Questions?

Feel free to open an issue with your question. We're here to help! 