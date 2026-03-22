"""
Project module - represents an Anamnesis flashcard project
"""

import json
from pathlib import Path
from typing import Dict, List, Any

import yaml


class Project:
    """Represents an Anamnesis project containing decks and cards."""
    
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.config_file = self.root_path / "_project.yml"
        self.decks_dir = self.root_path / "decks"
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load project configuration from _project.yml"""
        if self.config_file.exists():
            with open(self.config_file, "r") as f:
                return yaml.safe_load(f) or {}
        return {}
    
    def get_project_metadata(self) -> Dict[str, Any]:
        """Get project metadata from configuration"""
        return {
            "name": self.config.get("name", "Anamnesis Project"),
            "description": self.config.get("description", ""),
            "version": self.config.get("version", "0.1.1"),
        }
    
    def list_decks(self) -> List[str]:
        """List all deck directories in the project"""
        if not self.decks_dir.exists():
            return []
        return [d.name for d in self.decks_dir.iterdir() if d.is_dir()]
    
    @staticmethod
    def create_new(project_name: str) -> "Project":
        """Create a new Anamnesis project"""
        project_path = Path(project_name)
        project_path.mkdir(exist_ok=True)
        
        # Create directories
        (project_path / "decks").mkdir(exist_ok=True)
        (project_path / "build").mkdir(exist_ok=True)
        
        # Create _project.yml
        project_config = {
            "name": project_name,
            "description": "My Anamnesis flashcard project",
            "version": "0.1.1",
        }

        with open(project_path / "_project.yml", "w", encoding="utf-8") as f:
            yaml.dump(project_config, f, default_flow_style=False)
        
        # Create .gitignore
        gitignore_content = """# Anamnesis build artifacts
build/
dist/
*.pyc
__pycache__/
.Python
*.egg-info/
.DS_Store
.env
venv/
"""
        with open(project_path / ".gitignore", "w", encoding="utf-8") as f:
            f.write(gitignore_content)
        
        # Create example deck structure
        example_deck = project_path / "decks" / "getting_started"
        example_deck.mkdir(exist_ok=True)

        # Create _deck.yml
        deck_config = {
            "display_name": "Getting Started",
            "description": "Your first deck",
            "depends_on": [],
        }

        with open(example_deck / "_deck.yml", "w", encoding="utf-8") as f:
            yaml.dump(deck_config, f, default_flow_style=False)
        
        # Create example card files
        example_card_data = {
            "display_name": "Anamnesis Overview",
            "front": "What is Anamnesis?",
            "back": "Anamnesis is a platform for building and managing flashcard projects with dependency management.",
        }

        with open(example_deck / "what_is_anamnesis.json", "w", encoding="utf-8") as f:
            json.dump(example_card_data, f, indent=2)

        # Create card metadata file
        card_metadata = {
            "depends_on": None
        }

        with open(example_deck / "what_is_anamnesis.yml", "w", encoding="utf-8") as f:
            yaml.dump(card_metadata, f, default_flow_style=False)

        return Project(str(project_path))
