"""
Builder module - generates web interface for the project
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any
from .project import Project
from .deck import Deck
from .compiler import Compiler


class Builder:
    """Builds web interface from Anamnesis project"""
    
    def __init__(self, project_dir: str = "."):
        self.project = Project(project_dir)
        self.build_dir = self.project.root_path / "build"
        self.compiler = Compiler(project_dir)
    
    def build(self) -> None:
        """Build the web interface"""
        self.build_dir.mkdir(exist_ok=True)
        
        # Generate project manifest
        manifest = self._generate_manifest()
        
        # Write manifest
        with open(self.build_dir / "manifest.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        
        # Generate HTML
        self._generate_html()
        
        # Copy static assets
        self._copy_assets()
    
    def _generate_manifest(self) -> Dict[str, Any]:
        """Generate project manifest with all decks and cards"""
        deck_names = self.project.list_decks()
        deck_order = self.compiler.get_deck_order()
        
        decks_data = []
        for deck_name in deck_names:
            deck_path = self.project.decks_dir / deck_name
            deck = Deck(str(deck_path))
            
            decks_data.append({
                "id": deck_name,
                "metadata": deck.get_metadata(),
                "cards": deck.get_cards(),
            })
        
        return {
            "project": self.project.get_project_metadata(),
            "decks": decks_data,
            "deck_order": deck_order,
            "dependency_graph": self.compiler.get_dependency_graph(),
        }
    
    def _generate_html(self) -> None:
        """Generate main HTML file"""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Anamnesis - Flashcard Learning</title>
    <link rel="stylesheet" href="static/style.css">
</head>
<body>
    <div id="app">
        <nav class="navbar">
            <h1>Anamnesis</h1>
            <p id="project-title"></p>
        </nav>
        
        <main class="container">
            <div id="decks-view" class="view">
                <h2>Decks</h2>
                <div id="decks-list" class="decks-grid">
                    <!-- Dynamically populated -->
                </div>
            </div>
            
            <div id="deck-view" class="view hidden">
                <button class="back-btn" onclick="showDecksView()">&lt;&lt; Back to Decks</button>
                <h2 id="deck-title"></h2>
                <p id="deck-description"></p>
                <div class="deck-actions">
                    <button class="btn btn-primary" onclick="startLearning()">Learn</button>
                    <button class="btn btn-secondary" onclick="startTest()">Test</button>
                </div>
                <div id="cards-list" class="cards-list">
                    <!-- Dynamically populated -->
                </div>
            </div>
            
            <div id="learn-view" class="view hidden">
                <button class="back-btn" onclick="backToDeck()">&lt;&lt; Back to Deck</button>
                <h2>Learning Mode</h2>
                <div class="card-container">
                    <div class="card-counter">
                        <span id="current-card">1</span> / <span id="total-cards">10</span>
                    </div>
                    <div class="flashcard" onclick="flipCard(this)">
                        <div class="flashcard-inner">
                            <div class="flashcard-front" id="card-front"></div>
                            <div class="flashcard-back" id="card-back"></div>
                        </div>
                    </div>
                    <div class="card-navigation">
                        <button class="btn" onclick="prevCard()">&lt; Previous</button>
                        <button class="btn" onclick="nextCard()">Next &gt;</button>
                    </div>
                </div>
            </div>
            
            <div id="test-view" class="view hidden">
                <button class="back-btn" onclick="backToDeck()">&lt;&lt; Back to Deck</button>
                <h2>Test Mode</h2>
                <div class="test-container">
                    <div class="question-counter">
                        <span id="test-current">1</span> / <span id="test-total">10</span>
                    </div>
                    <div class="question-section">
                        <h3 id="question-text"></h3>
                        <div id="answer-options" class="answer-options">
                            <!-- Dynamically populated -->
                        </div>
                    </div>
                    <div class="test-navigation">
                        <button class="btn" onclick="prevQuestion()">&lt; Previous</button>
                        <button class="btn" onclick="nextQuestion()">Next &gt;</button>
                    </div>
                </div>
            </div>
        </main>
    </div>
    
    <script src="static/app.js"></script>
</body>
</html>
"""
        with open(self.build_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
    
    def _copy_assets(self) -> None:
        """Copy static assets (CSS, JS)"""
        static_dir = self.build_dir / "static"
        static_dir.mkdir(exist_ok=True)
        
        # Generate CSS
        css_content = """
:root {
    --primary-color: #3b82f6;
    --secondary-color: #10b981;
    --danger-color: #ef4444;
    --gray-light: #f3f4f6;
    --gray-dark: #1f2937;
    --border-radius: 8px;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background-color: #f9fafb;
    color: var(--gray-dark);
    line-height: 1.6;
}

.navbar {
    background-color: var(--primary-color);
    color: white;
    padding: 1.5rem 2rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.navbar h1 {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
}

.navbar p {
    opacity: 0.9;
    font-size: 0.9rem;
}

.container {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 1rem;
}

.view {
    display: none;
}

.view:not(.hidden) {
    display: block;
}

.hidden {
    display: none !important;
}

/* Decks Grid */
.decks-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 1.5rem;
}

.deck-card {
    background: white;
    border-radius: var(--border-radius);
    padding: 1.5rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    border: 2px solid transparent;
}

.deck-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.15);
    border-color: var(--primary-color);
}

.deck-card h3 {
    color: var(--primary-color);
    margin-bottom: 0.5rem;
}

.deck-card p {
    color: #6b7280;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

.deck-meta {
    display: flex;
    gap: 1rem;
    font-size: 0.85rem;
    color: #9ca3af;
}

/* Buttons */
.btn {
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: var(--border-radius);
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 500;
}

.btn-primary {
    background-color: var(--primary-color);
    color: white;
}

.btn-primary:hover {
    background-color: #2563eb;
    transform: translateY(-2px);
}

.btn-secondary {
    background-color: var(--secondary-color);
    color: white;
}

.btn-secondary:hover {
    background-color: #059669;
    transform: translateY(-2px);
}

.back-btn {
    padding: 0.5rem 1rem;
    color: var(--primary-color);
    background: none;
    border: none;
    cursor: pointer;
    font-size: 1rem;
    margin-bottom: 1rem;
}

.back-btn:hover {
    text-decoration: underline;
}

/* Flashcard */
.card-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 500px;
    gap: 2rem;
    margin-top: 2rem;
}

.card-counter {
    font-size: 1.1rem;
    color: #6b7280;
    font-weight: 500;
}

.flashcard {
    width: 100%;
    max-width: 600px;
    height: 400px;
    perspective: 1000px;
    cursor: pointer;
}

.flashcard-inner {
    position: relative;
    width: 100%;
    height: 100%;
    text-align: center;
    transition: transform 0.6s;
    transform-style: preserve-3d;
}

.flashcard.flipped .flashcard-inner {
    transform: rotateY(180deg);
}

.flashcard-front, .flashcard-back {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    border-radius: var(--border-radius);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.flashcard-front {
    background: linear-gradient(135deg, var(--primary-color), #60a5fa);
    color: white;
    font-size: 1.5rem;
    font-weight: 600;
}

.flashcard-back {
    background: linear-gradient(135deg, var(--secondary-color), #34d399);
    color: white;
    font-size: 1.25rem;
    transform: rotateY(180deg);
}

/* Cards List */
.cards-list {
    margin-top: 2rem;
}

.card-item {
    background: white;
    padding: 1rem;
    margin-bottom: 1rem;
    border-radius: var(--border-radius);
    border-left: 4px solid var(--primary-color);
}

.card-item strong {
    color: var(--primary-color);
}

/* Test Mode */
.test-container {
    background: white;
    padding: 2rem;
    border-radius: var(--border-radius);
    max-width: 800px;
    margin: 2rem auto;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.question-counter {
    color: #6b7280;
    margin-bottom: 1.5rem;
    font-weight: 500;
}

.question-section h3 {
    font-size: 1.5rem;
    margin-bottom: 2rem;
    color: var(--gray-dark);
}

.answer-options {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.answer-option {
    padding: 1rem;
    border: 2px solid #e5e7eb;
    border-radius: var(--border-radius);
    cursor: pointer;
    transition: all 0.3s ease;
    background: white;
}

.answer-option:hover {
    border-color: var(--primary-color);
    background-color: #eff6ff;
}

.answer-option.correct {
    background-color: #dcfce7;
    border-color: var(--secondary-color);
}

.answer-option.incorrect {
    background-color: #fee2e2;
    border-color: var(--danger-color);
}

/* Navigation */
.card-navigation, .test-navigation, .deck-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin-top: 2rem;
}

h2 {
    color: var(--gray-dark);
    margin-bottom: 1rem;
}

h3 {
    color: var(--gray-dark);
}
"""
        with open(static_dir / "style.css", "w", encoding="utf-8") as f:
            f.write(css_content)
        
        # Generate JavaScript
        js_content = """
let manifest = {};
let currentDeck = null;
let currentCardIndex = 0;
let currentTestIndex = 0;
let testAnswers = {};
let allDecks = [];

// Load manifest on page load
document.addEventListener('DOMContentLoaded', function() {
    fetch('manifest.json')
        .then(response => response.json())
        .then(data => {
            manifest = data;
            allDecks = data.decks || [];
            initializeApp();
        })
        .catch(error => console.error('Error loading manifest:', error));
});

function initializeApp() {
    const projectData = manifest.project || {};
    const projectTitle = document.getElementById('project-title');
    if (projectTitle) {
        projectTitle.textContent = projectData.description || '';
    }
    showDecksView();
}

function showDecksView() {
    hideAllViews();
    document.getElementById('decks-view').classList.remove('hidden');
    renderDecksList();
}

function renderDecksList() {
    const decksList = document.getElementById('decks-list');
    decksList.innerHTML = '';
    
    allDecks.forEach(deck => {
        const deckEl = document.createElement('div');
        deckEl.className = 'deck-card';
        deckEl.innerHTML = `
            <h3>${deck.metadata.name || deck.id}</h3>
            <p>${deck.metadata.description || 'No description'}</p>
            <div class="deck-meta">
                <span>📚 ${deck.cards.length} cards</span>
            </div>
        `;
        deckEl.onclick = () => selectDeck(deck.id);
        decksList.appendChild(deckEl);
    });
}

function selectDeck(deckId) {
    currentDeck = allDecks.find(d => d.id === deckId);
    if (currentDeck) {
        showDeckView();
    }
}

function showDeckView() {
    hideAllViews();
    document.getElementById('deck-view').classList.remove('hidden');
    
    const deck = currentDeck;
    document.getElementById('deck-title').textContent = deck.metadata.name || deck.id;
    document.getElementById('deck-description').textContent = deck.metadata.description || '';
    
    renderCardsList();
}

function renderCardsList() {
    const cardsList = document.getElementById('cards-list');
    cardsList.innerHTML = '';
    
    currentDeck.cards.forEach((card, index) => {
        const cardEl = document.createElement('div');
        cardEl.className = 'card-item';
        cardEl.innerHTML = `
            <strong>${index + 1}. ${card.front}</strong>
            <p>${card.back}</p>
        `;
        cardsList.appendChild(cardEl);
    });
}

function startLearning() {
    currentCardIndex = 0;
    hideAllViews();
    document.getElementById('learn-view').classList.remove('hidden');
    showCard();
}

function startTest() {
    currentTestIndex = 0;
    testAnswers = {};
    hideAllViews();
    document.getElementById('test-view').classList.remove('hidden');
    showTestQuestion();
}

function showCard() {
    if (currentCardIndex >= currentDeck.cards.length) {
        alert('You\\'ve completed the deck!');
        backToDeck();
        return;
    }
    
    const card = currentDeck.cards[currentCardIndex];
    document.getElementById('current-card').textContent = currentCardIndex + 1;
    document.getElementById('total-cards').textContent = currentDeck.cards.length;
    document.getElementById('card-front').textContent = card.front;
    document.getElementById('card-back').textContent = card.back;
    
    // Reset flip state
    document.querySelector('.flashcard').classList.remove('flipped');
}

function flipCard(element) {
    element.classList.toggle('flipped');
}

function nextCard() {
    currentCardIndex++;
    showCard();
}

function prevCard() {
    if (currentCardIndex > 0) {
        currentCardIndex--;
        showCard();
    }
}

function showTestQuestion() {
    if (currentTestIndex >= currentDeck.cards.length) {
        showTestResults();
        return;
    }
    
    const card = currentDeck.cards[currentTestIndex];
    document.getElementById('test-current').textContent = currentTestIndex + 1;
    document.getElementById('test-total').textContent = currentDeck.cards.length;
    document.getElementById('question-text').textContent = card.front;
    
    // Simple multiple choice - for now just show the answer with other cards mixed in
    const options = currentDeck.cards.map(c => c.back).sort(() => Math.random() - 0.5);
    const correctAnswer = card.back;
    
    const answerOptions = document.getElementById('answer-options');
    answerOptions.innerHTML = '';
    
    options.slice(0, 4).forEach(answer => {
        const btn = document.createElement('button');
        btn.className = 'answer-option btn';
        btn.textContent = answer;
        btn.onclick = () => selectAnswer(answer, correctAnswer, btn);
        answerOptions.appendChild(btn);
    });
}

function selectAnswer(selected, correct, element) {
    testAnswers[currentTestIndex] = selected;
    if (selected === correct) {
        element.classList.add('correct');
    } else {
        element.classList.add('incorrect');
    }
    
    // Disable all options after selection
    document.querySelectorAll('.answer-option').forEach(btn => btn.disabled = true);
}

function nextQuestion() {
    currentTestIndex++;
    showTestQuestion();
}

function prevQuestion() {
    if (currentTestIndex > 0) {
        currentTestIndex--;
        showTestQuestion();
    }
}

function showTestResults() {
    const correct = Object.entries(testAnswers).filter(([index, answer]) => {
        return answer === currentDeck.cards[index].back;
    }).length;
    
    alert(`Test completed!\\n\\nCorrect: ${correct}/${currentDeck.cards.length}\\nScore: ${Math.round(correct/currentDeck.cards.length*100)}%`);
    backToDeck();
}

function backToDeck() {
    showDeckView();
}

function hideAllViews() {
    document.querySelectorAll('.view').forEach(view => {
        view.classList.add('hidden');
    });
}
"""
        with open(static_dir / "app.js", "w", encoding="utf-8") as f:
            f.write(js_content)
    
    def serve(self, host: str = "127.0.0.1", port: int = 5000) -> None:
        """Serve the built web interface using SimpleHTTPServer"""
        import http.server
        import socketserver
        
        # Change to build directory
        original_dir = os.getcwd()
        os.chdir(self.build_dir)
        
        try:
            class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
                """HTTP handler that serves index.html for root and supports caching headers"""
                
                def log_message(self, format, *args):
                    """Suppress default logging"""
                    pass
                
                def end_headers(self):
                    """Add cache control headers"""
                    self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
                    super().end_headers()
                
                def do_GET(self):
                    """Handle GET requests"""
                    if self.path == '/':
                        self.path = '/index.html'
                    elif self.path.endswith('/'):
                        self.path = self.path + 'index.html'
                    return super().do_GET()
            
            # Suppress default server logging
            socketserver.TCPServer.allow_reuse_address = True
            
            with socketserver.TCPServer((host, port), QuietHTTPRequestHandler) as httpd:
                click = __import__('click')
                click.echo(f"✓ Build successful!")
                click.echo(f"  Web interface generated in 'build/' directory")
                click.echo(f"  Starting server at http://{host}:{port}")
                click.echo("  Press Ctrl+C to exit")
                click.echo()
                
                try:
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    click.echo("\n✗ Server stopped")
        finally:
            os.chdir(original_dir)
