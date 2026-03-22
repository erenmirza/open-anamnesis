"""
Card module - represents a single flashcard
"""

from typing import Dict, List, Any, Optional


class Card:
    """Represents a single flashcard with front/back content"""
    
    def __init__(self, card_data: Dict[str, Any]):
        """
        Initialize a card from a dictionary.
        
        Required fields:
        - id: Unique identifier for the card
        - front: Question or prompt
        - back: Answer or content
        
        Optional fields:
        - tags: List of tags for categorization
        - difficulty: Difficulty level (easy, medium, hard)
        - related_cards: List of related card IDs
        """
        self.id = card_data.get("id")
        self.front = card_data.get("front")
        self.back = card_data.get("back")
        self.tags = card_data.get("tags", [])
        self.difficulty = card_data.get("difficulty", "medium")
        self.related_cards = card_data.get("related_cards", [])
        self.metadata = card_data.get("metadata", {})
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert card to dictionary"""
        return {
            "id": self.id,
            "front": self.front,
            "back": self.back,
            "tags": self.tags,
            "difficulty": self.difficulty,
            "related_cards": self.related_cards,
            "metadata": self.metadata,
        }
    
    def validate(self) -> tuple[bool, List[str]]:
        """Validate card has all required fields"""
        errors = []
        
        if not self.id:
            errors.append("Card missing required field: id")
        
        if not self.front:
            errors.append("Card missing required field: front")
        
        if not self.back:
            errors.append("Card missing required field: back")
        
        if not isinstance(self.tags, list):
            errors.append(f"Card {self.id}: tags must be a list")
        
        if self.difficulty not in ["easy", "medium", "hard"]:
            errors.append(f"Card {self.id}: invalid difficulty level '{self.difficulty}'")
        
        if not isinstance(self.related_cards, list):
            errors.append(f"Card {self.id}: related_cards must be a list")
        
        return len(errors) == 0, errors
