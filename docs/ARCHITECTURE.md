# Architecture Overview

## Core Components

### 1. **Project** (`open_anamnesis/project.py`)
Represents an entire Anamnesis project.

**Responsibilities:**
- Manage project structure (decks, config)
- Load and parse project metadata
- Provide deck discovery

**Key Methods:**
- `create_new()` - Initialize new project with template structure
- `list_decks()` - Get all decks in project
- `get_project_metadata()` - Retrieve project info

### 2. **Deck** (`open_anamnesis/deck.py`)
Represents a collection of related flashcards.

**Responsibilities:**
- Load deck metadata (deck.yml)
- Load and manage cards
- Validate deck structure

**Key Methods:**
- `get_metadata()` - Get deck info
- `get_cards()` - Retrieve all cards
- `validate()` - Check deck integrity

### 3. **Card** (`open_anamnesis/card.py`)
Represents a single flashcard.

**Responsibilities:**
- Store front/back content
- Manage card metadata (tags, difficulty)
- Validate card data

**Key Methods:**
- `validate()` - Ensure required fields present
- `to_dict()` - Convert to dictionary

### 4. **Compiler** (`open_anamnesis/compiler.py`)
Validates entire project structure and content.

**Responsibilities:**
- Validate all YAML and JSON files
- Check for duplicate card IDs
- Verify deck dependencies
- Generate dependency graph

**Key Methods:**
- `compile()` - Full project validation
- `get_dependency_graph()` - Get deck relationships
- `get_deck_order()` - Return topological sort

### 5. **Builder** (`open_anamnesis/builder.py`)
Generates web interface from project.

**Responsibilities:**
- Create manifest.json from project
- Generate HTML/CSS/JS for web interface
- Start development server

**Key Methods:**
- `build()` - Generate all static files
- `serve()` - Launch web server

### 6. **CLI** (`open_anamnesis/cli.py`)
Command-line interface for user interactions.

**Commands:**
- `anamnesis init` - Create new project
- `anamnesis compile` - Validate project
- `anamnesis build` - Build and serve

## Data Flow

```
User Input (CLI)
    ↓
CLI Handler (cli.py)
    ↓
Project Loader (project.py)
    ↓
Compiler (compiler.py) - Validation
    ↓
Builder (builder.py) - Web Generation
    ↓
Web Interface / Static Files
```

## File Structure

### Project Layout

```
my_project/
├── _project.yml             # Project metadata
├── decks/
│   ├── deck_1/
│   │   ├── _deck.yml        # Deck metadata
│   │   ├── card_1.json      # Card content
│   │   ├── card_1.yml       # Card metadata
│   │   ├── card_2.json
│   │   └── card_2.yml
│   └── deck_2/
│       ├── _deck.yml
│       ├── card_a.json
│       └── card_a.yml
└── build/                   # Generated files
    ├── index.html
    ├── manifest.json
    └── static/
        ├── style.css
        └── app.js
```

### Config Files

**_project.yml**
```yaml
name: Project Name
description: Description
version: 1.0.0
```

**_deck.yml** (in each deck directory)
```yaml
display_name: Deck Name
description: Description
depends_on:
  - prerequisite_deck
```

**card_name.json** (individual card files)
```json
{
  "display_name": "Card Title",
  "front": "Question text",
  "back": "Answer text"
}
```

**card_name.yml** (card metadata)
```yaml
depends_on: other_card_id  # or null for first card
```

## Implementation Details

### Validation Pipeline

1. **Project.yml** - Parse and validate YAML
2. **Deck Lists** - Find all decks in project
3. **Deck Structure** - Verify deck.yml and cards.json exist
4. **Card Content** - Validate each card's required fields
5. **Dependencies** - Check deck references are valid
6. **Uniqueness** - Ensure card IDs don't duplicate

### Dependency Resolution

Uses topological sorting to determine card learning order:

```python
def get_deck_order():
    # Depth-first traversal of dependency graph
    # Returns decks in order: prerequisites before dependents
```

### Web Generation

1. Create `manifest.json` from compiled project
2. Generate HTML structure
3. Create CSS styling
4. Create JavaScript interactions
5. Start Flask/HTTP server

## Extension Points

### Adding New Card Metadata

1. Add field to Card class
2. Update cards.json schema documentation
3. Update validation rules in Card.validate()
4. Update web interface to display new field

### Custom Card Types

1. Extend Card class
2. Implement custom validation
3. Update builder to render differently
4. Update web interface JavaScript

### Alternative Learning Modes

1. Add new mode to Builder
2. Create HTML view and CSS
3. Implement JavaScript interactions
4. Add selection UI

## Testing Strategy

**Unit Tests** - Test individual classes in isolation
**Integration Tests** - Test full workflow from CLI to web output
**Validation Tests** - Test error detection and reporting

See `tests/test_core.py` for example tests.
