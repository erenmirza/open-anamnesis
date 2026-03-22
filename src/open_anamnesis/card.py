"""
Card module - represents a single flashcard
"""

from typing import Dict, List, Any, Optional

# Character limits for card fields
MAX_DISPLAY_NAME_LENGTH = 60
MAX_FRONT_LENGTH = 200
MAX_BACK_LENGTH = 500


class Card:
    """Represents a single flashcard with front/back content"""

    def __init__(self, card_data: Dict[str, Any]):
        """
        Initialize a card from a dictionary.

        Required fields:
        - display_name: Human-readable name for the card
        - front: Question or prompt
        - back: Answer or content

        Optional fields:
        - id: Unique identifier (auto-generated from filename if not provided)
        - depends_on: Single card ID this card depends on
        - metadata: Additional metadata
        """
        self.id = card_data.get("id")
        self.display_name = card_data.get("display_name")
        self.front = card_data.get("front")
        self.back = card_data.get("back")
        self.depends_on = card_data.get("depends_on")
        self.metadata = card_data.get("metadata", {})
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert card to dictionary"""
        return {
            "id": self.id,
            "display_name": self.display_name,
            "front": self.front,
            "back": self.back,
            "depends_on": self.depends_on,
            "metadata": self.metadata,
        }
    
    def validate(self) -> tuple[bool, List[str]]:
        """Validate card has all required fields and character limits"""
        errors = []

        card_ref = f"Card {self.id}" if self.id else "Card"

        # Check required fields
        if not self.display_name:
            errors.append(f"{card_ref}: missing required field: display_name")
        elif len(self.display_name) > MAX_DISPLAY_NAME_LENGTH:
            errors.append(
                f"{card_ref}: display_name exceeds maximum length of {MAX_DISPLAY_NAME_LENGTH} characters "
                f"(current: {len(self.display_name)})"
            )

        if not self.front:
            errors.append(f"{card_ref}: missing required field: front")
        elif len(self.front) > MAX_FRONT_LENGTH:
            errors.append(
                f"{card_ref}: front exceeds maximum length of {MAX_FRONT_LENGTH} characters "
                f"(current: {len(self.front)})"
            )

        if not self.back:
            errors.append(f"{card_ref}: missing required field: back")
        elif len(self.back) > MAX_BACK_LENGTH:
            errors.append(
                f"{card_ref}: back exceeds maximum length of {MAX_BACK_LENGTH} characters "
                f"(current: {len(self.back)})"
            )

        return len(errors) == 0, errors
