# Open Anamnesis

Open-source flashcards as code. Build and manage flashcard projects with dependency management, validation, and a web-based learning interface.

![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue) ![License](https://img.shields.io/badge/License-MIT-green)

## Features

- **Structured Decks**: Organize flashcards with dependency management
- **Validation**: Compile and validate YAML/JSON for correctness
- **Web Interface**: Auto-generated learning platform with Learn and Test modes
- **Dependencies**: Learn in the correct order with prerequisite tracking

## Quick Start

```bash
# Install
pip install open-anamnesis

# Initialize project
anamnesis init my_project
cd my_project

# Validate
anamnesis-compile

# Build and launch
anamnesis-build
# Visit http://127.0.0.1:5000
```

## Project Structure

```
my_project/
├── project.yml          # name, description, version
├── decks/
│   └── deck_name/
│       ├── deck.yml     # name, description, depends_on
│       └── cards.json   # array of cards
└── build/               # generated files
```

**Card Schema (cards.json)**
```json
[
  {
    "id": "unique_id",
    "front": "Question",
    "back": "Answer",
    "tags": ["optional"],
    "difficulty": "easy|medium|hard"
  }
]
```

## Commands

```bash
anamnesis init [PROJECT_NAME]              # Initialize new project
anamnesis-compile [-d PROJECT_DIR]         # Validate project
anamnesis-build [-d DIR] [-p PORT]         # Build and serve (default: port 5000)
```

## Validation

The compiler checks for:
- Valid YAML and JSON syntax
- Required card fields (id, front, back)
- Unique card IDs within decks
- Valid dependency resolution
- No circular dependencies

## Development

See [docs/GUIDE.md](docs/GUIDE.md) for development setup and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for system overview.

## License

MIT License - see [LICENSE](LICENSE) file.
