"""
Tests for the Anamnesis package
"""

import pytest
import tempfile
import json
from pathlib import Path

import yaml

from open_anamnesis.project import Project
from open_anamnesis.deck import Deck
from open_anamnesis.card import Card, MAX_DISPLAY_NAME_LENGTH, MAX_FRONT_LENGTH, MAX_BACK_LENGTH
from open_anamnesis.compiler import Compiler
from open_anamnesis.builder import Builder


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
            assert (project_path / ".gitignore").exists()

    def test_list_decks(self):
        """Test listing decks in a project"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            project = Project.create_new(str(project_path))

            decks = project.list_decks()
            assert "getting_started" in decks

    def test_get_project_metadata(self):
        """Test getting project metadata"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            project = Project.create_new(str(project_path))

            metadata = project.get_project_metadata()
            assert "name" in metadata
            assert "description" in metadata
            assert "version" in metadata


class TestCard:
    def test_card_creation(self):
        """Test creating a card"""
        card_data = {
            "id": "test_001",
            "display_name": "Test Card",
            "front": "Test question?",
            "back": "Test answer"
        }

        card = Card(card_data)
        assert card.id == "test_001"
        assert card.display_name == "Test Card"
        assert card.front == "Test question?"
        assert card.back == "Test answer"

    def test_card_validation_valid(self):
        """Test card validation with valid card"""
        valid_card = Card({
            "id": "test_001",
            "display_name": "Test Card",
            "front": "Question?",
            "back": "Answer",
        })
        is_valid, errors = valid_card.validate()
        assert is_valid
        assert len(errors) == 0

    def test_card_validation_missing_display_name(self):
        """Test card validation with missing display_name"""
        invalid_card = Card({
            "id": "test_002",
            "front": "Question?",
            "back": "Answer",
        })
        is_valid, errors = invalid_card.validate()
        assert not is_valid
        assert any("display_name" in err for err in errors)

    def test_card_validation_missing_front(self):
        """Test card validation with missing front"""
        invalid_card = Card({
            "id": "test_003",
            "display_name": "Test",
            "back": "Answer",
        })
        is_valid, errors = invalid_card.validate()
        assert not is_valid
        assert any("front" in err for err in errors)

    def test_card_validation_missing_back(self):
        """Test card validation with missing back"""
        invalid_card = Card({
            "id": "test_004",
            "display_name": "Test",
            "front": "Question?",
        })
        is_valid, errors = invalid_card.validate()
        assert not is_valid
        assert any("back" in err for err in errors)

    def test_card_validation_display_name_too_long(self):
        """Test card validation with display_name exceeding max length"""
        long_name = "a" * (MAX_DISPLAY_NAME_LENGTH + 1)
        card = Card({
            "id": "test_005",
            "display_name": long_name,
            "front": "Question?",
            "back": "Answer",
        })
        is_valid, errors = card.validate()
        assert not is_valid
        assert any("display_name exceeds" in err for err in errors)

    def test_card_validation_front_too_long(self):
        """Test card validation with front exceeding max length"""
        long_front = "a" * (MAX_FRONT_LENGTH + 1)
        card = Card({
            "id": "test_006",
            "display_name": "Test",
            "front": long_front,
            "back": "Answer",
        })
        is_valid, errors = card.validate()
        assert not is_valid
        assert any("front exceeds" in err for err in errors)

    def test_card_validation_back_too_long(self):
        """Test card validation with back exceeding max length"""
        long_back = "a" * (MAX_BACK_LENGTH + 1)
        card = Card({
            "id": "test_007",
            "display_name": "Test",
            "front": "Question?",
            "back": long_back,
        })
        is_valid, errors = card.validate()
        assert not is_valid
        assert any("back exceeds" in err for err in errors)

    def test_card_to_dict(self):
        """Test converting card to dictionary"""
        card_data = {
            "id": "test_008",
            "display_name": "Test Card",
            "front": "Question?",
            "back": "Answer",
        }
        card = Card(card_data)
        result = card.to_dict()

        assert result["id"] == "test_008"
        assert result["display_name"] == "Test Card"
        assert result["front"] == "Question?"
        assert result["back"] == "Answer"


class TestDeck:
    def test_deck_creation(self):
        """Test creating a deck"""
        with tempfile.TemporaryDirectory() as tmpdir:
            deck_path = Path(tmpdir)
            deck_path.mkdir(exist_ok=True)

            # Create _deck.yml
            deck_config = {
                "name": "Test Deck",
                "description": "Test deck",
                "depends_on": []
            }
            with open(deck_path / "_deck.yml", "w") as f:
                yaml.dump(deck_config, f)

            # Create individual card files
            card_data = {
                "display_name": "Test Card 1",
                "front": "Q1?",
                "back": "A1"
            }
            with open(deck_path / "card_001.json", "w") as f:
                json.dump(card_data, f)

            # Create card.yml
            card_metadata = {"depends_on": None}
            with open(deck_path / "card_001.yml", "w") as f:
                yaml.dump(card_metadata, f)

            deck = Deck(str(deck_path))
            assert deck.name == deck_path.name
            assert len(deck.get_cards()) == 1
            assert deck.get_cards()[0]["id"] == "card_001"

    def test_deck_validation_missing_deck_yml(self):
        """Test deck validation with missing _deck.yml"""
        with tempfile.TemporaryDirectory() as tmpdir:
            deck_path = Path(tmpdir)
            deck_path.mkdir(exist_ok=True)

            deck = Deck(str(deck_path))
            is_valid, errors = deck.validate()

            assert not is_valid
            assert any("_deck.yml" in err for err in errors)

    def test_deck_validation_no_cards(self):
        """Test deck validation with no card files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            deck_path = Path(tmpdir)
            deck_path.mkdir(exist_ok=True)

            deck_config = {
                "name": "Empty Deck",
                "description": "No cards",
                "depends_on": []
            }
            with open(deck_path / "_deck.yml", "w") as f:
                yaml.dump(deck_config, f)

            deck = Deck(str(deck_path))
            is_valid, errors = deck.validate()

            assert not is_valid
            assert any("No card files" in err for err in errors)

    def test_get_deck_metadata(self):
        """Test getting deck metadata"""
        with tempfile.TemporaryDirectory() as tmpdir:
            deck_path = Path(tmpdir)
            deck_path.mkdir(exist_ok=True)

            deck_config = {
                "name": "Test Deck",
                "description": "A test deck",
                "depends_on": ["other_deck"]
            }
            with open(deck_path / "_deck.yml", "w") as f:
                yaml.dump(deck_config, f)

            card_data = {"display_name": "Card", "front": "Q?", "back": "A"}
            with open(deck_path / "card.json", "w") as f:
                json.dump(card_data, f)

            with open(deck_path / "card.yml", "w") as f:
                yaml.dump({"depends_on": None}, f)

            deck = Deck(str(deck_path))
            metadata = deck.get_metadata()

            assert metadata["name"] == "Test Deck"
            assert metadata["description"] == "A test deck"
            assert "other_deck" in metadata["depends_on"]
            assert metadata["card_count"] == 1


class TestCompiler:
    def test_compile_valid_project(self):
        """Test compiling a valid project"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            project = Project.create_new(str(project_path))

            compiler = Compiler(str(project_path))
            results = compiler.compile()

            assert results["success"]
            assert results["decks_count"] == 1
            assert results["cards_count"] >= 1
            assert len(results["errors"]) == 0

    def test_compile_missing_project_yml(self):
        """Test compiling with missing project.yml"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create empty directory
            compiler = Compiler(str(tmpdir))
            results = compiler.compile()

            assert not results["success"]
            assert any("project.yml" in err for err in results["errors"])

    def test_compile_invalid_deck_dependency(self):
        """Test compiling with invalid deck dependency"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            project = Project.create_new(str(project_path))

            # Modify deck to depend on non-existent deck
            deck_path = project_path / "decks" / "getting_started"
            deck_config = {
                "name": "Getting Started",
                "description": "Test",
                "depends_on": ["non_existent_deck"]
            }
            with open(deck_path / "_deck.yml", "w") as f:
                yaml.dump(deck_config, f)

            compiler = Compiler(str(project_path))
            results = compiler.compile()

            assert not results["success"]
            assert any("non_existent_deck" in err for err in results["errors"])

    def test_get_dependency_graph(self):
        """Test getting dependency graph"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            project = Project.create_new(str(project_path))

            compiler = Compiler(str(project_path))
            graph = compiler.get_dependency_graph()

            assert isinstance(graph, dict)
            assert "getting_started" in graph

    def test_get_deck_order(self):
        """Test getting deck order via topological sort"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            project = Project.create_new(str(project_path))

            compiler = Compiler(str(project_path))
            order = compiler.get_deck_order()

            assert isinstance(order, list)
            assert "getting_started" in order


class TestBuilder:
    def test_build_creates_manifest(self):
        """Test that building creates manifest.json"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            project = Project.create_new(str(project_path))

            builder = Builder(str(project_path))
            builder.build()

            manifest_path = project_path / "build" / "manifest.json"
            assert manifest_path.exists()

            with open(manifest_path) as f:
                manifest = json.load(f)

            assert "project" in manifest
            assert "decks" in manifest
            assert "deck_order" in manifest
            assert "dependency_graph" in manifest

    def test_build_creates_html(self):
        """Test that building creates index.html"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            project = Project.create_new(str(project_path))

            builder = Builder(str(project_path))
            builder.build()

            html_path = project_path / "build" / "index.html"
            assert html_path.exists()

    def test_build_creates_static_assets(self):
        """Test that building creates static assets"""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            project = Project.create_new(str(project_path))

            builder = Builder(str(project_path))
            builder.build()

            static_dir = project_path / "build" / "static"
            assert static_dir.exists()
            assert (static_dir / "style.css").exists()
            assert (static_dir / "app.js").exists()


if __name__ == "__main__":
    pytest.main([__file__])
