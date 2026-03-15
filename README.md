# Open Anamnesis

A dbt-like platform for building and managing flashcard projects with dependency management, validation, and a web-based learning interface.

Open-source flashcards as code. Write, import, and compose decks in your repo to generate a local learning website.

<img src="https://img.shields.io/badge/Python-3.8%2B-blue" alt="Python 3.8+">
<img src="https://img.shields.io/badge/License-MIT-green" alt="License">

## 🎯 Features

- **Project Organization**: Organize flashcards into structured decks with dependency management
- **Validation**: Compile and validate all files (YAML, JSON) for correctness
- **Web Interface**: Auto-generated learning interface with multiple modes
- **Learning Modes**: 
  - **Learn Mode**: Read through cards in dependency order
  - **Test Mode**: Self-test with multiple choice questions
- **Dependency Management**: Define deck dependencies and learn in the correct order

## 📦 Installation

```bash
pip install open-anamnesis
```

Or for development:

```bash
git clone https://github.com/yourusername/open-anamnesis.git
cd open-anamnesis
pip install -e .
```

## 🚀 Getting Started

Follow these steps to create your first Anamnesis flashcard project.

### Step 1: Create a Repository

```bash
# Create a new directory for your project
mkdir my_study_project
cd my_study_project

# Initialize git (optional but recommended)
git init
```

### Step 2: Setup Python Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal, indicating the virtual environment is active.

### Step 3: Install Anamnesis

```bash
pip install open-anamnesis
```

Verify installation:
```bash
anamnesis --version
```

### Step 4: Initialize Your Project

```bash
anamnesis init my_project
cd my_project
```

This creates your project structure:

```
my_project/
├── project.yml              # Project metadata
├── .gitignore               # Git ignore file
├── decks/                   # Your decks directory
│   └── getting_started/     # Example deck
│       ├── deck.yml         # Deck metadata
│       └── cards.json       # Flashcards
└── build/                   # Generated build artifacts
```

### Step 5: Create Your Decks

Create a new deck by adding a directory under `decks/`:

```bash
mkdir decks/python_basics
```

Create `decks/python_basics/deck.yml`:
```yaml
name: "Python Basics"
description: "Learn Python fundamentals"
depends_on:
  - getting_started
```

Create `decks/python_basics/cards.json`:
```json
[
  {
    "id": "card_001",
    "front": "What is a Python function?",
    "back": "A reusable block of code that performs a specific task",
    "tags": ["functions", "basics"],
    "difficulty": "easy"
  },
  {
    "id": "card_002",
    "front": "What's the difference between a list and a tuple?",
    "back": "Lists are mutable (can be changed), tuples are immutable (cannot be changed)",
    "tags": ["data-structures", "basics"],
    "difficulty": "medium"
  }
]
```

### Step 6: Validate Your Project

Compile your project to validate all files:

```bash
anamnesis-compile
```

Expected output:
```
✓ Compilation successful!
  - Validated 3 deck(s)
  - Validated 12 card(s)
  - No errors found
```

If there are errors, the compiler will show you exactly what to fix.

### Step 7: Build and Launch

Generate the web interface and start the learning platform:

```bash
anamnesis-build
```

Expected output:
```
✓ Build successful!
  Web interface generated in 'build/' directory
  Starting server at http://127.0.0.1:5000
  Press Ctrl+C to exit
```

Open your browser to **http://127.0.0.1:5000** and start learning! 🎓

## ✨ Quick Example Workflow

```bash
# 1. Create project
mkdir biology_study && cd biology_study

# 2. Virtual environment
python -m venv venv && source venv/bin/activate  # Linux/Mac
# Or: venv\Scripts\activate  # Windows

# 3. Install
pip install open-anamnesis

# 4. Initialize
anamnesis init .

# 5. Edit your decks (create decks/your_deck/deck.yml and cards.json)

# 6. Validate
anamnesis-compile

# 7. Build and learn
anamnesis-build
# Visit http://127.0.0.1:5000
```

## 📚 Project Structure

### project.yml

Project metadata file:

```yaml
name: "My Study Project"
description: "A comprehensive learning project"
version: "1.0.0"
```

### deck.yml

Deck metadata file (in each deck directory):

```yaml
name: "Deck Name"
description: "Description of what this deck covers"
depends_on:
  - prerequisite_deck_1
  - prerequisite_deck_2
```

### cards.json

Card data file (in each deck directory):

```json
[
  {
    "id": "unique_card_id",
    "front": "Question or prompt",
    "back": "Answer or content",
    "tags": ["tag1", "tag2"],
    "difficulty": "easy|medium|hard",
    "related_cards": ["card_002", "card_003"],
    "metadata": {}
  }
]
```

**Card Fields:**
- `id` (required): Unique identifier for the card
- `front` (required): Question or prompt text
- `back` (required): Answer or content text
- `tags` (optional): List of tags for categorization
- `difficulty` (optional): Difficulty level - "easy", "medium", or "hard"
- `related_cards` (optional): List of related card IDs
- `metadata` (optional): Custom metadata

## 📖 Usage

### Commands

#### `anamnesis init [PROJECT_NAME]`

Initialize a new Anamnesis project with example structure.

```bash
anamnesis init my_project
```

#### `anamnesis-compile [OPTIONS]`

Validate all project files and check for errors.

Options:
- `-d, --project-dir`: Project directory (default: current directory)

```bash
anamnesis-compile -d ./my_project
```

#### `anamnesis-build [OPTIONS]`

Build and launch the web interface.

Options:
- `-d, --project-dir`: Project directory (default: current directory)
- `-p, --port`: Port to run server on (default: 5000)
- `--host`: Host to bind to (default: 127.0.0.1)

```bash
anamnesis-build -d ./my_project -p 8000
```

## 🌐 Web Interface

The generated web interface provides:

### Decks View
- Browse all available decks
- See card count and description for each deck
- Click a deck to view its cards

### Deck View
- View all cards in the deck
- Choose learning mode or test mode

### Learn Mode
- Flip through cards in dependency order
- Click cards to reveal answers
- Navigate with Previous/Next buttons

### Test Mode
- Multiple choice questions based on cards
- Get scored based on correct answers
- Review your performance

## 🔄 Workflow Example

```bash
# 1. Initialize project
anamnesis init biology_study

# 2. Create deck structures
mkdir biology_study/decks/cells
mkdir biology_study/decks/genetics

# 3. Add deck metadata
echo 'name: Cells
description: Learn about cell structure and function' > biology_study/decks/cells/deck.yml

# 4. Add cards
cat > biology_study/decks/cells/cards.json << 'EOF'
[
  {
    "id": "cell_001",
    "front": "What is the cell membrane?",
    "back": "A lipid bilayer that controls what enters and exits the cell"
  }
]
EOF

# 5. Validate
anamnesis-compile

# 6. Build and study
anamnesis-build
```

## 🛠️ Development

### Setup Development Environment

```bash
git clone https://github.com/yourusername/open-anamnesis.git
cd open-anamnesis
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

### Running Tests

```bash
pytest
```

## 📋 Configuration Files

### .gitignore

The `anamnesis init` command creates a `.gitignore` file that excludes:
- `build/` - Generated build artifacts
- `dist/` - Distribution files
- Python cache files
- Virtual environment directories

## 🚨 Validation Rules

The compiler checks:
- ✅ All YAML files are valid YAML
- ✅ All JSON files are valid JSON  
- ✅ All required fields are present in cards
- ✅ Card IDs are unique within each deck
- ✅ Deck dependencies resolve correctly
- ✅ No circular dependencies

## 🎓 Best Practices

1. **Use meaningful deck names**: Makes it easy to navigate
2. **Keep card fronts concise**: Consider them like flashcard prompts
3. **Include tags**: Help organize related cards
4. **Set difficulty levels**: Help prioritize what to study
5. **Use dependencies wisely**: Ensure prerequisite knowledge before advanced decks

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Happy Learning! 📚✨**
