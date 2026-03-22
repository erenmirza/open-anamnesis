# Anamnesis Examples

This directory contains example Anamnesis projects to help you learn and get started.

## cli_guide

A complete interactive guide that teaches you how to use Anamnesis through flashcards!

### What's inside:

- **Getting Started**: Introduction to Anamnesis and installation
- **CLI Commands**: Learn the command-line interface (init, compile, build)
- **Project Structure**: Understanding file organization
- **Creating Content**: How to create decks and cards with dependencies

### Try it out:

```bash
cd cli_guide
anamnesis compile
anamnesis build
```

Then visit http://127.0.0.1:5000 to see the interactive learning interface!

## Creating Your Own Project

Use the cli_guide as a reference when building your own flashcard projects:

```bash
# Start from scratch
anamnesis init my_project
cd my_project

# Or copy and modify the example
cp -r examples/cli_guide my_custom_project
cd my_custom_project
# Edit the decks and cards to your needs
```

## Tips

- Each deck is a separate directory under `decks/`
- Cards are pairs of `.json` (content) and `.yml` (metadata) files
- Use dependencies to create learning paths
- Run `anamnesis-compile` often to catch errors early
