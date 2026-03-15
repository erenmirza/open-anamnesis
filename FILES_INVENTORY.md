# 📋 Project Files Inventory

## Core Package Files

### Main Modules
| File | Purpose |
|------|---------|
| `open_anamnesis/__init__.py` | Package initialization, exports main classes |
| `open_anamnesis/cli.py` | Command-line interface with 3 main commands |
| `open_anamnesis/project.py` | Project structure management and initialization |
| `open_anamnesis/deck.py` | Deck model with YAML config and validation |
| `open_anamnesis/card.py` | Card data model with metadata |
| `open_anamnesis/compiler.py` | Project validation and dependency resolution |
| `open_anamnesis/builder.py` | Web interface generation and Flask server |

## Configuration Files

| File | Purpose |
|------|---------|
| `setup.py` | Traditional Python package setup |
| `pyproject.toml` | Modern Python packaging (PEP 518) |
| `requirements.txt` | Direct pip dependencies |
| `.gitignore` | Git ignore patterns |

## Documentation

| File | Purpose |
|------|---------|
| `README.md` | Main documentation - features, installation, usage |
| `CONTRIBUTING.md` | Contribution guidelines for developers |
| `docs/ARCHITECTURE.md` | System design and component overview |
| `docs/GUIDE.md` | Developer guide and setup instructions |
| `PROJECT_SETUP_SUMMARY.md` | This project overview |

## Tests

| File | Purpose |
|------|---------|
| `tests/__init__.py` | Test package initialization |
| `tests/test_core.py` | Unit tests for all core modules |

## Examples

| File | Purpose |
|------|---------|
| `examples/README.md` | Examples overview and instructions |
| `examples/python_learning_path/project.yml` | Example project configuration |
| `examples/python_learning_path/decks/01_basics/deck.yml` | Example deck config (no dependencies) |
| `examples/python_learning_path/decks/01_basics/cards.json` | 5 example flashcards |
| `examples/python_learning_path/decks/02_functions/deck.yml` | Deck with dependency on 01_basics |
| `examples/python_learning_path/decks/02_functions/cards.json` | 5 function-related cards |
| `examples/python_learning_path/decks/03_oop/deck.yml` | Deck with dependency on 02_functions |
| `examples/python_learning_path/decks/03_oop/cards.json` | 5 OOP-related cards |

## Key Features by File

### CLI (`cli.py`)
- `anamnesis init` - Create new project with templates
- `anamnesis-compile` - Validate all files and dependencies
- `anamnesis-build` - Generate web interface and start server

### Project (`project.py`)
- Load/parse project.yml
- Create new projects with scaffolding
- Discover decks in project
- Generate project metadata

### Deck (`deck.py`)
- Load/parse deck.yml and cards.json
- Validate deck structure
- Manage deck dependencies
- Return cards in order

### Card (`card.py`)
- Load card data with validation
- Support metadata (tags, difficulty, etc.)
- Validate required fields
- Convert to/from dictionaries

### Compiler (`compiler.py`)
- Validate all YAML/JSON files
- Check required fields in cards
- Detect duplicate card IDs
- Resolve and validate dependencies
- Generate dependency graph
- Topological sort for learning order

### Builder (`builder.py`)
- Generate manifest.json from project
- Create HTML template
- Generate CSS (responsive design)
- Generate JavaScript (interactivity)
- Start Flask/HTTP web server
- Support Learn and Test modes

## Generated Files (on `anamnesis-build`)

```
build/
├── index.html          # Web interface
├── manifest.json       # Project data in JSON
└── static/
    ├── style.css       # Styling
    └── app.js          # Frontend logic
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| click | >=8.0.0 | CLI framework |
| pyyaml | >=5.4.0 | YAML parsing |
| jsonschema | >=4.0.0 | JSON validation |
| jinja2 | >=3.0.0 | Template rendering |
| flask | >=2.0.0 | Web server |

## Lines of Code Summary

- **Core Modules**: ~800 lines
- **CLI**: ~130 lines
- **Tests**: ~100+ lines
- **Documentation**: ~500+ lines
- **Total**: ~1500+ lines of well-documented code

## Ready-to-Use Templates

### Project Template (created by `anamnesis init`)
- Directories: project root, decks/, build/
- Files: project.yml (with example config), .gitignore
- Example deck: getting_started/ with sample card

### Example Project (in examples/)
- 3-deck Python learning path
- Demonstrates dependency system
- ~15 total flashcards
- Ready to compile and test

## Development Setup Completed

- ✅ Virtual environment compatible
- ✅ Development dependencies listed
- ✅ Type hints throughout
- ✅ Docstrings on all functions
- ✅ Unit tests included
- ✅ Code style guidelines (Black/Flake8)
- ✅ Error handling and logging

---

**Total Files Created: 25+**
**Total Functionality: Production-ready flashcard platform**
