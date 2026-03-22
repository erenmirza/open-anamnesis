# Developer Guide

This guide helps developers understand and contribute to the Anamnesis project.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/open-anamnesis/open-anamnesis.git
cd open-anamnesis
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e .
```

### 3. Verify Installation

```bash
# Test CLI works
anamnesis --version

# Run tests
pytest tests/
```

## Project Structure

```
open-anamnesis/
├── src/
│   └── open_anamnesis/
│       ├── __init__.py         # Package exports
│       ├── cli.py              # Command-line interface
│       ├── project.py          # Project management
│       ├── deck.py             # Deck management
│       ├── card.py             # Card definition
│       ├── compiler.py         # Validation logic
│       ├── builder.py          # Web generation
│       ├── templates/
│       │   └── index.html      # HTML template
│       └── static/
│           ├── style.css       # Styles
│           └── app.js          # JavaScript
├── tests/
│   ├── test_core.py            # Unit tests
│   └── __init__.py
├── examples/
│   └── cli_guide/              # Example project
├── docs/
│   ├── ARCHITECTURE.md         # System design
│   └── GUIDE.md                # This file
├── pyproject.toml              # Modern Python packaging
└── README.md                   # User documentation
```

## Development Workflow

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Edit files in `open_anamnesis/`
   - Add tests in `tests/`
   - Update documentation

3. **Test your changes**
   ```bash
   pytest tests/
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "Add feature: description"
   git push origin feature/your-feature-name
   ```

5. **Create a pull request**

## Code Style

### Type Hints

Use type hints in function signatures:

```python
def load_cards(deck_path: str) -> List[Dict[str, Any]]:
    """Load cards from JSON file."""
    pass
```

### Docstrings

Use docstrings for all public functions:

```python
def validate(self) -> Tuple[bool, List[str]]:
    """
    Validate deck structure and content.
    
    Returns:
        Tuple of (is_valid: bool, errors: List[str])
    """
    pass
```

## Common Tasks

### Adding a New CLI Command

1. Add function in `open_anamnesis/cli.py`:

```python
@main.command()
@click.option("--option", "-o", default="default")
def new_command(option):
    """Description of command."""
    click.echo("Hello")
```

2. Update setup.py entry points

3. Test the command

### Adding a New Validation Rule

1. Add check in appropriate class (`Deck.validate()`, `Card.validate()`, etc.)

2. Add to Compiler validation pipeline

3. Add test case in `tests/test_core.py`

### Extending Card Metadata

1. Update `Card` class to accept new field

2. Update schema documentation in README

3. Update validation logic

4. Update web interface to display it

## Testing

### Running Tests

```bash
# All tests
pytest

# Single test file
pytest tests/test_core.py

# Single test
pytest tests/test_core.py::TestCard::test_card_validation

# With verbose output
pytest -v
```

### Writing Tests

```python
def test_feature():
    """Test description."""
    # Arrange
    expected = "value"
    
    # Act
    result = function_under_test()
    
    # Assert
    assert result == expected
```

## Debugging

### Print Debugging

```python
import sys
print("Debug info:", value, file=sys.stderr)
```

### Using Debugger

```python
import pdb; pdb.set_trace()
```

### Checking Manifest

After building, inspect the generated manifest:

```bash
cat build/manifest.json | python -m json.tool
```

## Key Files to Understand

### cli.py
- Entry points for all commands
- User-facing error messaging
- Error validation and reporting

### project.py
- Project structure initialization
- Config file management
- Deck discovery

### compiler.py
- Project validation logic
- Dependency resolution
- Error collection

### builder.py
- Manifest generation
- HTML/CSS/JS generation
- Server setup

## Common Issues

### Import Errors

If you get `ModuleNotFoundError`:

```bash
# Reinstall in development mode
pip install -e .
```

### YAML Parse Errors

Ensure YAML files are properly formatted:

```bash
# Validate YAML
python -c "import yaml; yaml.safe_load(open('file.yml'))"
```

### JSON Parse Errors

Ensure JSON files are valid:

```bash
# Validate JSON
python -m json.tool deck/cards.json
```

## Performance Considerations

1. **Lazy Loading** - Load decks/cards only when needed
2. **Caching** - Cache manifest in memory during compile
3. **Streaming** - For large projects, consider streaming output

## Security Considerations

1. **File Paths** - Always use `pathlib.Path` for file operations
2. **Input Validation** - Validate user inputs before use
3. **JSON/YAML Parsing** - Use safe loaders only

## Release Process

1. Update version in `setup.py` and `pyproject.toml`
2. Update CHANGELOG (if exists)
3. Run full test suite
4. Tag release: `git tag v0.1.0`
5. Push tag: `git push origin v0.1.0`
6. Build and publish: `python -m build && twine upload dist/*`

## Dependencies

- **click** - CLI framework
- **pyyaml** - YAML parsing
- **jinja2** - Template rendering (future use)
- Built-in HTTP server for serving the web interface

## Getting Help

- Check existing issues on GitHub
- Read ARCHITECTURE.md for system overview
- Review existing code for patterns
- Ask for clarification on pull requests

## Contributing Guidelines

1. Follow existing code style
2. Add tests for new features
3. Update documentation
4. Keep commits atomic and descriptive
5. Reference issues in commit messages

Thank you for contributing! 🎉
