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
    updateDeckStats();
}

function updateDeckStats() {
    const stats = document.getElementById('deck-stats');
    const totalDecks = allDecks.length;
    const totalCards = allDecks.reduce((sum, deck) => sum + deck.cards.length, 0);
    stats.textContent = `${totalDecks} deck${totalDecks !== 1 ? 's' : ''} • ${totalCards} total cards`;
}

function renderDecksList() {
    const decksList = document.getElementById('decks-list');
    decksList.innerHTML = '';

    allDecks.forEach((deck, index) => {
        const deckEl = document.createElement('div');
        deckEl.className = 'deck-card';
        deckEl.style.animationDelay = `${index * 0.05}s`;

        const icon = getDeckIcon(index);
        deckEl.innerHTML = `
            <h3>${icon} ${deck.metadata.name || deck.id}</h3>
            <p>${deck.metadata.description || 'No description available'}</p>
            <div class="deck-meta">
                <span>${deck.cards.length} card${deck.cards.length !== 1 ? 's' : ''}</span>
            </div>
        `;
        deckEl.onclick = () => selectDeck(deck.id);
        decksList.appendChild(deckEl);
    });
}

function getDeckIcon(index) {
    const icons = ['📚', '🎯', '🧠', '💡', '🚀', '⭐', '🔥', '💫', '🎨', '🌟'];
    return icons[index % icons.length];
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
    document.getElementById('deck-description').textContent = deck.metadata.description || 'No description available';

    renderCardsList();
}

function renderCardsList() {
    const cardsList = document.getElementById('cards-list');
    cardsList.innerHTML = '';

    currentDeck.cards.forEach((card, index) => {
        const cardEl = document.createElement('div');
        cardEl.className = 'card-item';
        cardEl.innerHTML = `
            <strong>Card ${index + 1}</strong>
            <p><strong>Q:</strong> ${card.front}</p>
            <p><strong>A:</strong> ${card.back}</p>
        `;
        cardsList.appendChild(cardEl);
    });
}

function startLearning() {
    currentCardIndex = 0;
    hideAllViews();
    document.getElementById('learn-view').classList.remove('hidden');
    showCard();
    updateLearningProgress();
}

function startTest() {
    currentTestIndex = 0;
    testAnswers = {};
    hideAllViews();
    document.getElementById('test-view').classList.remove('hidden');
    showTestQuestion();
    updateTestProgress();
}

function updateLearningProgress() {
    const progress = ((currentCardIndex + 1) / currentDeck.cards.length) * 100;
    document.getElementById('learn-progress').style.width = progress + '%';
}

function updateTestProgress() {
    const progress = ((currentTestIndex + 1) / currentDeck.cards.length) * 100;
    document.getElementById('test-progress').style.width = progress + '%';
}

function showCard() {
    if (currentCardIndex >= currentDeck.cards.length) {
        showCompletionMessage('Learning session complete!', 'You\'ve reviewed all cards in this deck.');
        backToDeck();
        return;
    }

    const card = currentDeck.cards[currentCardIndex];
    document.getElementById('current-card').textContent = currentCardIndex + 1;
    document.getElementById('total-cards').textContent = currentDeck.cards.length;
    document.getElementById('card-front').textContent = card.front;
    document.getElementById('card-back').textContent = card.back;

    // Reset flip state
    const flashcard = document.querySelector('.flashcard');
    flashcard.classList.remove('flipped');

    updateLearningProgress();
}

function flipCard(element) {
    element.classList.toggle('flipped');
}

function nextCard() {
    if (currentCardIndex < currentDeck.cards.length - 1) {
        currentCardIndex++;
        showCard();
    } else {
        showCard(); // This will trigger the completion message
    }
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

    const correctAnswer = card.back;

    // Get other answers from different cards
    const otherAnswers = currentDeck.cards
        .filter(c => c.back !== correctAnswer)
        .map(c => c.back);

    // Randomly select 3 incorrect options (or fewer if not enough cards)
    const numIncorrect = Math.min(3, otherAnswers.length);
    const shuffledOthers = otherAnswers.sort(() => Math.random() - 0.5);
    const incorrectOptions = shuffledOthers.slice(0, numIncorrect);

    // Combine correct answer with incorrect options and shuffle
    const options = [correctAnswer, ...incorrectOptions].sort(() => Math.random() - 0.5);

    const answerOptions = document.getElementById('answer-options');
    answerOptions.innerHTML = '';

    options.forEach((answer, index) => {
        const btn = document.createElement('button');
        btn.className = 'answer-option';
        btn.textContent = answer;
        btn.style.animationDelay = `${index * 0.05}s`;
        btn.onclick = () => selectAnswer(answer, correctAnswer, btn);
        answerOptions.appendChild(btn);
    });

    updateTestProgress();
}

function selectAnswer(selected, correct, element) {
    testAnswers[currentTestIndex] = selected;

    // Add visual feedback
    if (selected === correct) {
        element.classList.add('correct');
    } else {
        element.classList.add('incorrect');
        // Show correct answer
        document.querySelectorAll('.answer-option').forEach(btn => {
            if (btn.textContent === correct) {
                btn.classList.add('correct');
            }
        });
    }

    // Disable all options after selection
    document.querySelectorAll('.answer-option').forEach(btn => {
        btn.disabled = true;
        btn.style.cursor = 'not-allowed';
    });
}

function nextQuestion() {
    if (currentTestIndex < currentDeck.cards.length - 1) {
        currentTestIndex++;
        showTestQuestion();
    } else {
        showTestResults();
    }
}

function prevQuestion() {
    if (currentTestIndex > 0) {
        currentTestIndex--;
        // Clear previous answer if going back
        const wasAnswered = testAnswers.hasOwnProperty(currentTestIndex);
        if (wasAnswered) {
            delete testAnswers[currentTestIndex];
        }
        showTestQuestion();
    }
}

function showTestResults() {
    const correct = Object.entries(testAnswers).filter(([index, answer]) => {
        return answer === currentDeck.cards[index].back;
    }).length;

    const total = currentDeck.cards.length;
    const percentage = Math.round((correct / total) * 100);

    let emoji = '🎉';
    let message = 'Great job!';

    if (percentage === 100) {
        emoji = '🏆';
        message = 'Perfect score!';
    } else if (percentage >= 80) {
        emoji = '🌟';
        message = 'Excellent work!';
    } else if (percentage >= 60) {
        emoji = '👍';
        message = 'Good effort!';
    } else {
        emoji = '📚';
        message = 'Keep practicing!';
    }

    showCompletionMessage(
        `${emoji} Test Complete!`,
        `${message}\n\nScore: ${correct}/${total} (${percentage}%)`
    );
    backToDeck();
}

function showCompletionMessage(title, message) {
    // Simple alert for now - could be enhanced with a custom modal
    alert(title + '\n\n' + message);
}

function backToDeck() {
    showDeckView();
}

function hideAllViews() {
    document.querySelectorAll('.view').forEach(view => {
        view.classList.add('hidden');
    });
}

// Keyboard navigation
document.addEventListener('keydown', function(e) {
    const learnView = document.getElementById('learn-view');
    const testView = document.getElementById('test-view');

    if (!learnView.classList.contains('hidden')) {
        if (e.key === 'ArrowLeft') {
            prevCard();
        } else if (e.key === 'ArrowRight') {
            nextCard();
        } else if (e.key === ' ' || e.key === 'Enter') {
            e.preventDefault();
            const flashcard = document.querySelector('.flashcard');
            flipCard(flashcard);
        }
    } else if (!testView.classList.contains('hidden')) {
        if (e.key === 'ArrowLeft') {
            prevQuestion();
        } else if (e.key === 'ArrowRight') {
            nextQuestion();
        }
    }
});
