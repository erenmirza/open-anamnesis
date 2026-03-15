# Contributing to Anamnesis

Thank you for your interest in contributing to Anamnesis! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions with other contributors.

## Ways to Contribute

1. **Report Bugs** - Open an issue describing the problem
2. **Suggest Features** - Open an issue describing your idea
3. **Fix Bugs** - Submit a pull request with a fix
4. **Add Features** - Submit a pull request with new functionality
5. **Improve Documentation** - Fix typos, add examples, clarify explanations

## Getting Started

### For Bug Reports and Feature Requests

1. Check existing issues first
2. Open a new issue with clear description
3. Include reproduction steps for bugs
4. Include your environment details

### For Code Contributions

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes following code style guidelines
4. Add tests for new functionality
5. Run test suite: `pytest`
6. Commit with clear messages: `git commit -m "Add feature: description"`
7. Push to your fork: `git push origin feature/your-feature`
8. Open a pull request to main

## Development Setup

```bash
git clone https://github.com/yourusername/open-anamnesis.git
cd open-anamnesis
python -m venv venv
source venv/bin/activate
pip install -e .
pip install pytest black flake8 mypy
```

## Code Style

### Format Code

```bash
black open_anamnesis/
```

### Check Linting

```bash
flake8 open_anamnesis/
```

### Type Hints

Use type hints for all functions:

```python
def my_function(arg: str) -> List[str]:
    """Description."""
    pass
```

### Documentation

Write docstrings for all public functions and classes:

```python
def my_function(arg: str) -> bool:
    """
    Brief description.
    
    Extended description if needed.
    
    Args:
        arg: Description of arg
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When something is invalid
    """
```

## Testing

### Run Tests

```bash
pytest tests/
```

### Write Tests

Add tests to `tests/test_core.py` for new functionality:

```python
def test_my_feature():
    """Test description."""
    # Arrange
    input_data = ...
    
    # Act
    result = function_to_test(input_data)
    
    # Assert
    assert result == expected_value
```

Aim for at least 80% code coverage.

## Commit Messages

Use clear, descriptive commit messages:

- ✅ `Add feature: support for card metadata`
- ✅ `Fix bug: incorrect dependency resolution`
- ✅ `Docs: add architecture overview`
- ✅ `Refactor: simplify validation logic`
- ❌ `fixed stuff`
- ❌ `updates`

Reference issues when applicable:

```
Fix deck validation error handling

- Improve error messages for invalid decks
- Add unit tests for validation

Fixes #123
```

## Pull Request Process

1. **Title** - Clear, descriptive title
2. **Description** - Explain what changes and why
3. **Testing** - Confirm all tests pass
4. **Documentation** - Update docs if needed
5. **Code Style** - Follow style guidelines
6. **Self Review** - Review your own changes first

### PR Description Template

```markdown
## Description
Brief description of changes.

## Related Issue
Fixes #issue_number

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Other (describe)

## Testing
Describe how you tested the changes.

## Checklist
- [ ] Tests pass (`pytest`)
- [ ] Code formatted (`black`)
- [ ] Code linted (`flake8`)
- [ ] Types checked (`mypy`)
- [ ] Documentation updated
- [ ] Commit messages clear
```

## Documentation

### Updating README

- Keep examples working and up-to-date
- Add complex features to docs/
- Include code snippets with proper syntax highlighting

### Adding to Docs

Create or update markdown files in `docs/`:

- `ARCHITECTURE.md` - System design
- `GUIDE.md` - Developer guide
- `CONTRIBUTING.md` - This file

## Reporting Security Issues

Please report security issues privately to the maintainers. Do not open public issues for security vulnerabilities.

## Licensing

By contributing to Anamnesis, you agree that your contributions are licensed under the MIT License.

## Questions?

- Open an issue with tag `question`
- Check existing issues and discussions
- Review documentation in `/docs`

## Recognition

Contributors will be recognized in:
- CHANGELOG.md
- GitHub contributor list
- Release notes

Thank you for contributing! 🙌
