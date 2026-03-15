"""
Compiler module - validates all project files
"""

from pathlib import Path
from typing import Dict, List, Any
import yaml
import json
from .project import Project
from .deck import Deck
from jsonschema import validate, ValidationError


class Compiler:
    """Compiles and validates Anamnesis projects"""
    
    def __init__(self, project_dir: str = "."):
        self.project = Project(project_dir)
        self.errors = []
        self.warnings = []
    
    def compile(self) -> Dict[str, Any]:
        """Compile and validate entire project"""
        self.errors = []
        self.warnings = []
        
        decks_count = 0
        cards_count = 0
        
        try:
            # Validate project.yml
            self._validate_project_yml()
            
            # Get all decks
            deck_names = self.project.list_decks()
            decks_count = len(deck_names)
            
            # Validate each deck
            for deck_name in deck_names:
                deck_path = self.project.decks_dir / deck_name
                deck = Deck(str(deck_path))
                
                # Validate deck structure
                is_valid, deck_errors = deck.validate()
                self.errors.extend([f"Deck '{deck_name}': {e}" for e in deck_errors])
                
                cards_count += len(deck.get_cards())
            
            # Validate dependencies
            self._validate_dependencies()
            
        except Exception as e:
            self.errors.append(f"Compilation error: {e}")
        
        success = len(self.errors) == 0
        
        return {
            "success": success,
            "decks_count": decks_count,
            "cards_count": cards_count,
            "errors": self.errors,
            "warnings": self.warnings,
        }
    
    def _validate_project_yml(self) -> None:
        """Validate project.yml structure"""
        if not self.project.config_file.exists():
            self.errors.append("Missing project.yml in project root")
            return
        
        try:
            with open(self.project.config_file, "r") as f:
                config = yaml.safe_load(f)
            
            # Check for required fields
            if config is None:
                self.errors.append("project.yml is empty")
            elif not isinstance(config, dict):
                self.errors.append("project.yml must contain a dictionary")
            
        except yaml.YAMLError as e:
            self.errors.append(f"Invalid YAML in project.yml: {e}")
        except Exception as e:
            self.errors.append(f"Error reading project.yml: {e}")
    
    def _validate_dependencies(self) -> None:
        """Validate deck dependencies are valid"""
        deck_names = self.project.list_decks()
        
        for deck_name in deck_names:
            deck_path = self.project.decks_dir / deck_name
            deck = Deck(str(deck_path))
            
            depends_on = deck.config.get("depends_on", [])
            for dep in depends_on:
                if dep not in deck_names:
                    self.errors.append(
                        f"Deck '{deck_name}' depends on unknown deck '{dep}'"
                    )
    
    def get_dependency_graph(self) -> Dict[str, List[str]]:
        """Get dependency graph for all decks"""
        graph = {}
        deck_names = self.project.list_decks()
        
        for deck_name in deck_names:
            deck_path = self.project.decks_dir / deck_name
            deck = Deck(str(deck_path))
            graph[deck_name] = deck.config.get("depends_on", [])
        
        return graph
    
    def get_deck_order(self) -> List[str]:
        """Get decks in dependency order (topological sort)"""
        graph = self.get_dependency_graph()
        visited = set()
        order = []
        
        def visit(node):
            if node in visited:
                return
            visited.add(node)
            for dep in graph.get(node, []):
                visit(dep)
            order.append(node)
        
        for deck in graph:
            visit(deck)
        
        return order
