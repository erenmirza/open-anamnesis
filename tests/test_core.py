"""
Tests for the Anamnesis package
"""

import pytest
import tempfile
import json
from pathlib import Path
from src.project import Project
from src.deck import Deck
from src.card import Card
from src.compiler import Compiler


class TestProject:
    def test_create_new_project(self):
        """Test creating a new project"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_name = "test_project"
            project_path = Path(tmpdir) / project_name
            
            project = Project.create_new(str(project_path))
            
            assert project_path.exists()
            assert (project_path / "project.yml").exists()
            assert (project_path / "decks").exists()
            assert (project_path / "build").exists()
    
    def test_list_decks(self):
        """Test listing decks in a project"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            project = Project.create_new(str(project_path))
            
            decks = project.list_decks()
            assert "getting_started" in decks


class TestCard:
    def test_card_creation(self):
        """Test creating a card"""
        card_data = {
            "id": "test_001",
            "front": "Test question?",
            "back": "Test answer",
            "tags": ["test"],
            "difficulty": "easy"
        }
        
        card = Card(card_data)
        assert card.id == "test_001"
        assert card.front == "Test question?"
        assert card.back == "Test answer"
    
    def test_card_validation(self):
        """Test card validation"""
        # Valid card
        valid_card = Card({
            "id": "test_001",
            "front": "Question?",
            "back": "Answer",
        })
        is_valid, errors = valid_card.validate()
        assert is_valid
        assert len(errors) == 0
        
        # Invalid card - missing front
        invalid_card = Card({
            "id": "test_002",
            "back": "Answer",
        })
        is_valid, errors = invalid_card.validate()
        assert not is_valid
        assert len(errors) > 0


class TestDeck:
    def test_deck_creation(self):
        """Test creating a deck"""
        with tempfile.TemporaryDirectory() as tmpdir:
            deck_path = Path(tmpdir)
            deck_path.mkdir(exist_ok=True)
            
            # Create deck.yml
            import yaml
            deck_config = {
                "name": "Test Deck",
                "description": "Test deck",
                "depends_on": []
            }
            with open(deck_path / "deck.yml", "w") as f:
                yaml.dump(deck_config, f)
            
            # Create cards.json
            cards = [{
                "id": "card_001",
                "front": "Q1?",
                "back": "A1"
            }]
            with open(deck_path / "cards.json", "w") as f:
                json.dump(cards, f)
            
            deck = Deck(str(deck_path))
            assert deck.name == deck_path.name
            assert len(deck.get_cards()) == 1


class TestCompiler:
    def test_compile_project(self):
        """Test compiling a project"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            project = Project.create_new(str(project_path))
            
            compiler = Compiler(str(project_path))
            results = compiler.compile()
            
            assert results["success"]
            assert results["decks_count"] == 1
            assert results["cards_count"] >= 1


if __name__ == "__main__":
    pytest.main([__file__])
