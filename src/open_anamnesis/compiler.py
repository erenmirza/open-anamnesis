"""
Compiler module - validates all project files
"""

from pathlib import Path
from typing import Dict, List, Any

import yaml

from .project import Project
from .deck import Deck

# Project constraints
MAX_CARDS_PER_DECK = 9


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
            # Validate _project.yml
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

                # Validate maximum cards per deck
                card_count = len(deck.get_cards())
                if card_count > MAX_CARDS_PER_DECK:
                    self.errors.append(
                        f"Deck '{deck_name}': contains {card_count} cards, "
                        f"maximum allowed is {MAX_CARDS_PER_DECK}"
                    )

                cards_count += card_count
            
            # Validate deck dependencies
            self._validate_dependencies()

            # Check for circular deck dependencies
            self._check_circular_deck_dependencies()

            # Validate card dependencies
            self._validate_card_dependencies()

            # Check for circular card dependencies
            self._check_circular_card_dependencies()

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
        """Validate _project.yml structure"""
        if not self.project.config_file.exists():
            self.errors.append("Missing _project.yml in project root")
            return

        try:
            with open(self.project.config_file, "r") as f:
                config = yaml.safe_load(f)

            # Check for required fields
            if config is None:
                self.errors.append("_project.yml is empty")
                return
            elif not isinstance(config, dict):
                self.errors.append("_project.yml must contain a dictionary")
                return

            # Validate required fields
            if "name" not in config:
                self.errors.append("_project.yml: missing required field 'name'")
            elif not isinstance(config["name"], str) or not config["name"].strip():
                self.errors.append("_project.yml: 'name' must be a non-empty string")

            # Validate optional but expected fields
            if "description" in config and not isinstance(config["description"], str):
                self.errors.append("_project.yml: 'description' must be a string")

            if "version" in config and not isinstance(config["version"], str):
                self.errors.append("_project.yml: 'version' must be a string")

        except yaml.YAMLError as e:
            self.errors.append(f"Invalid YAML in _project.yml: {e}")
        except Exception as e:
            self.errors.append(f"Error reading _project.yml: {e}")
    
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

    def _validate_card_dependencies(self) -> None:
        """Validate card dependencies are valid"""
        deck_names = self.project.list_decks()

        for deck_name in deck_names:
            deck_path = self.project.decks_dir / deck_name
            deck = Deck(str(deck_path))
            cards = deck.get_cards()

            # Build a set of card IDs in this deck
            card_ids = {card["id"] for card in cards}

            # Check each card's dependencies
            first_card_found = False
            for card in cards:
                card_id = card["id"]
                depends_on = card.get("depends_on")

                # Check if this is the first card (no dependency)
                if depends_on is None:
                    if first_card_found:
                        self.errors.append(
                            f"Deck '{deck_name}': Multiple cards have no dependency. Only the first card should have no dependency."
                        )
                    first_card_found = True
                else:
                    # Cards can only have one dependency (must be a string)
                    if not isinstance(depends_on, str):
                        self.errors.append(
                            f"Deck '{deck_name}', Card '{card_id}': depends_on must be a single card ID (string), not a list"
                        )
                        continue

                    # Check that the dependency exists in this deck
                    if depends_on not in card_ids:
                        self.errors.append(
                            f"Deck '{deck_name}', Card '{card_id}': depends on unknown card '{depends_on}'"
                        )

                    # Check that card doesn't depend on itself
                    if depends_on == card_id:
                        self.errors.append(
                            f"Deck '{deck_name}', Card '{card_id}': cannot depend on itself"
                        )

            # Ensure at least one card has no dependency (first card)
            if cards and not first_card_found:
                self.errors.append(
                    f"Deck '{deck_name}': No first card found. At least one card must have no dependency."
                )

    def _check_circular_deck_dependencies(self) -> None:
        """Check for circular dependencies in decks"""
        deck_names = self.project.list_decks()
        graph = self.get_dependency_graph()

        def has_cycle(node, visited, rec_stack):
            visited.add(node)
            rec_stack.add(node)

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor, visited, rec_stack):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        for deck in deck_names:
            visited = set()
            rec_stack = set()
            if has_cycle(deck, visited, rec_stack):
                self.errors.append(f"Circular dependency detected involving deck '{deck}'")
                break  # Report once

    def _check_circular_card_dependencies(self) -> None:
        """Check for circular dependencies in cards within each deck"""
        deck_names = self.project.list_decks()

        for deck_name in deck_names:
            deck_path = self.project.decks_dir / deck_name
            deck = Deck(str(deck_path))
            cards = deck.get_cards()

            # Build card dependency graph
            graph = {}
            for card in cards:
                card_id = card["id"]
                depends_on = card.get("depends_on")
                if depends_on:
                    graph[card_id] = [depends_on]
                else:
                    graph[card_id] = []

            # Check for cycles
            def has_cycle(node, visited, rec_stack):
                visited.add(node)
                rec_stack.add(node)

                for neighbor in graph.get(node, []):
                    if neighbor not in visited:
                        if has_cycle(neighbor, visited, rec_stack):
                            return True
                    elif neighbor in rec_stack:
                        return True

                rec_stack.remove(node)
                return False

            for card in cards:
                card_id = card["id"]
                visited = set()
                rec_stack = set()
                if has_cycle(card_id, visited, rec_stack):
                    self.errors.append(
                        f"Deck '{deck_name}': Circular dependency detected involving card '{card_id}'"
                    )
                    break  # Report once per deck
    
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
