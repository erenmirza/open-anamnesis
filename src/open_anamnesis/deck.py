"""
Deck module - represents a deck containing cards
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Tuple

import yaml


class Deck:
    """Represents a deck containing flashcards"""

    def __init__(self, deck_path: str):
        self.deck_path = Path(deck_path)
        self.name = self.deck_path.name
        self.config_file = self.deck_path / "_deck.yml"
        self.config = self._load_config()
        self.cards = self._load_cards()

    def _load_config(self) -> Dict[str, Any]:
        """Load deck configuration from _deck.yml"""
        if self.config_file.exists():
            with open(self.config_file, "r") as f:
                return yaml.safe_load(f) or {}
        return {
            "display_name": self.name,
            "description": "",
            "depends_on": [],
        }

    def _load_cards(self) -> List[Dict[str, Any]]:
        """Load individual card files from deck directory"""
        cards = []

        # Find all .json files in the deck directory (except deck.json and cards.json)
        for card_file in sorted(self.deck_path.glob("*.json")):
            if card_file.name in ["deck.json", "cards.json"]:
                continue

            try:
                # Load card data
                with open(card_file, "r") as f:
                    card_data = json.load(f)

                # Generate card ID from filename (without .json)
                card_id = card_file.stem
                card_data["id"] = card_id

                # Load card metadata (depends_on) from .yml file
                card_yml = card_file.with_suffix(".yml")
                if card_yml.exists():
                    with open(card_yml, "r") as f:
                        metadata = yaml.safe_load(f) or {}
                        card_data["depends_on"] = metadata.get("depends_on")
                else:
                    card_data["depends_on"] = None

                cards.append(card_data)
            except Exception as e:
                print(f"Warning: Could not load card {card_file.name}: {e}")

        return cards
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get deck metadata"""
        return {
            "id": self.name,
            "name": self.config.get("display_name", self.name),
            "description": self.config.get("description", ""),
            "depends_on": self.config.get("depends_on", []),
            "card_count": len(self.cards),
        }
    
    def get_cards(self) -> List[Dict[str, Any]]:
        """Get all cards in the deck"""
        return self.cards
    
    def validate(self) -> Tuple[bool, List[str]]:
        """Validate deck structure and content"""
        errors = []

        # Check if _deck.yml exists
        if not self.config_file.exists():
            errors.append(f"Missing _deck.yml in {self.name}")

        # Check if there are any card files
        card_files = list(self.deck_path.glob("*.json"))
        card_files = [f for f in card_files if f.name not in ["deck.json", "cards.json"]]

        if not card_files:
            errors.append(f"No card files found in {self.name}")

        # Validate cards structure
        try:
            for i, card in enumerate(self.cards):
                card_errors = self._validate_card(card, i)
                errors.extend(card_errors)
        except Exception as e:
            errors.append(f"Error validating cards in {self.name}: {e}")

        # Validate dependencies format
        depends_on = self.config.get("depends_on", [])
        if not isinstance(depends_on, list):
            errors.append(f"Invalid depends_on format in {self.name}")

        return len(errors) == 0, errors
    
    def _validate_card(self, card: Dict[str, Any], index: int) -> List[str]:
        """Validate individual card structure"""
        errors = []

        # Use Card class validation for field requirements and character limits
        from .card import Card
        card_obj = Card(card)
        is_valid, card_errors = card_obj.validate()
        errors.extend([f"{self.name}: {e}" for e in card_errors])

        # Check that id is unique
        card_id = card.get("id")
        if card_id:
            duplicates = [i for i, c in enumerate(self.cards)
                         if c.get("id") == card_id and i != index]
            if duplicates:
                errors.append(f"Duplicate card ID: {card_id} in {self.name}")

        return errors
