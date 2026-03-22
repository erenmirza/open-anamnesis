"""
Open Anamnesis: A dbt-like platform for building and managing flashcard projects
"""

__version__ = "0.1.2"

from .project import Project
from .deck import Deck
from .card import Card

__all__ = ["Project", "Deck", "Card"]
