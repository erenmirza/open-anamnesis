# Open Anamnesis

Open-source flashcards as code. Build and manage flashcard projects with dependency management, validation, and a web-based learning interface.

## Example

- **Website Generated From Example**: [Example Project](https://erenmirza.github.io/open-anamnesis)


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
anamnesis compile

# Build and launch
anamnesis build
# Visit http://127.0.0.1:5000
```

## Project Structure

```
my_project/
├── _project.yml                # name, description, version
├── decks/
│   └── deck_name/
│       ├── _deck.yml           # display_name, description, depends_on
│       ├── card_name.json      # card front and back
│       └── card_name.yml       # card depends_on
└── build/                      # generated files
```

**Card Schema**

Each card consists of two files:

`card_name.json`:
```json
{
  "display_name": "Card Title",
  "front": "Question",
  "back": "Answer"
}
```

`card_name.yml`:
```yaml
depends_on: other_card_id  # or null for first card
```

**Character Limits**
- `display_name`: 60 characters
- `front`: 200 characters
- `back`: 500 characters

## Commands

```bash
anamnesis init [PROJECT_NAME]              # Initialize new project
anamnesis compile [-d PROJECT_DIR]         # Validate project
anamnesis build [-d DIR] [-p PORT]         # Build and serve (default: port 5000)
```

## Validation

The compiler validates:
- **Syntax**: Valid YAML and JSON
- **Required fields**: display_name, front, back for all cards
- **Character limits**: display_name (60), front (200), back (500)
- **Unique IDs**: Card IDs must be unique within each deck
- **Dependencies**:
  - Decks can depend on multiple decks
  - Cards depend on exactly one card (or null for first card)
  - Cards cannot reference cards in other decks
  - Each deck must have exactly one first card

## Development

See [docs/GUIDE.md](docs/GUIDE.md) for development setup and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for system overview.

## License

MIT License - see [LICENSE](LICENSE) file.
