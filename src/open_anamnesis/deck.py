"""
Deck module - represents a deck containing cards
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional


class Deck:
    """Represents a deck containing flashcards"""
    
    def __init__(self, deck_path: str):
        self.deck_path = Path(deck_path)
        self.name = self.deck_path.name
        self.config_file = self.deck_path / "deck.yml"
        self.cards_file = self.deck_path / "cards.json"
        self.config = self._load_config()
        self.cards = self._load_cards()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load deck configuration from deck.yml"""
        if self.config_file.exists():
            with open(self.config_file, "r") as f:
                return yaml.safe_load(f) or {}
        return {
            "name": self.name,
            "description": "",
            "depends_on": [],
        }
    
    def _load_cards(self) -> List[Dict[str, Any]]:
        """Load cards from cards.json"""
        if self.cards_file.exists():
            with open(self.cards_file, "r") as f:
                return json.load(f)
        return []
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get deck metadata"""
        return {
            "id": self.name,
            "name": self.config.get("name", self.name),
            "description": self.config.get("description", ""),
            "depends_on": self.config.get("depends_on", []),
            "card_count": len(self.cards),
        }
    
    def get_cards(self) -> List[Dict[str, Any]]:
        """Get all cards in the deck"""
        return self.cards
    
    def validate(self) -> tuple[bool, List[str]]:
        """Validate deck structure and content"""
        errors = []
        
        # Check if deck.yml exists
        if not self.config_file.exists():
            errors.append(f"Missing deck.yml in {self.name}")
        
        # Check if cards.json exists
        if not self.cards_file.exists():
            errors.append(f"Missing cards.json in {self.name}")
        
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
        
        required_fields = ["id", "front", "back"]
        for field in required_fields:
            if field not in card:
                errors.append(f"Card {index} in {self.name} missing required field: {field}")
        
        # Check that id is unique
        card_id = card.get("id")
        if card_id:
            duplicates = [i for i, c in enumerate(self.cards) 
                         if c.get("id") == card_id and i != index]
            if duplicates:
                errors.append(f"Duplicate card ID: {card_id} in {self.name}")
        
        return errors
