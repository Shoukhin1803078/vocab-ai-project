from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

# Sample word data structure (you'll need to expand this with your full word list)
words = [
    {
        "word": "aberrant",
        "type": "adjective",
        "english_meaning": "markedly different from an accepted norm",
        "bangla_meaning": "স্বাভাবিক থেকে ব্যতিক্রম",
        "hindi_meaning": "असामान्य, विचलित",
        "japanese_meaning": "異常な",
        "example": "When the financial director started screaming and throwing food at his co-workers, the police had to come in to deal with his aberrant behavior.",
        "memorized": False
    },
    # Add more words here
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_words')
def get_words():
    filter_type = request.args.get('filter', 'all')
    if filter_type == 'all':
        return jsonify(words)
    elif filter_type == 'memorized':
        return jsonify([word for word in words if word['memorized']])
    else:  # remaining
        return jsonify([word for word in words if not word['memorized']])

@app.route('/toggle_memorized/<word>')
def toggle_memorized(word):
    for w in words:
        if w['word'] == word:
            w['memorized'] = not w['memorized']
            return jsonify({'success': True})
    return jsonify({'success': False})

# HTML template string
template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Magoosh Vocabulary Learning</title>
    <style>
        /* CSS styles */
        :root {
            --primary-color: #4a90e2;
            --secondary-color: #f5f5f5;
            --text-color: #333;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f2f5;
        }

        .language-popup {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }

        .language-popup.active {
            display: flex;
        }

        .popup-content {
            background-color: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 1rem;
        }

        .header {
            background-color: var(--primary-color);
            color: white;
            padding: 1rem;
            text-align: center;
            margin-bottom: 2rem;
        }

        .controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .filter-buttons {
            display: flex;
            gap: 1rem;
        }

        button {
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            background-color: var(--primary-color);
            color: white;
            transition: background-color 0.3s;
        }

        button:hover {
            background-color: #357abd;
        }

        .word-card {
            background-color: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s;
        }

        .word-card:hover {
            transform: translateY(-3px);
        }

        .word-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }

        .word-title {
            font-size: 1.5rem;
            color: var(--primary-color);
        }

        .word-type {
            color: #666;
            font-style: italic;
        }

        .meanings {
            margin: 1rem 0;
        }

        .meaning {
            margin: 0.5rem 0;
        }

        .example {
            margin-top: 1rem;
            font-style: italic;
            color: #666;
        }

        .memorized {
            background-color: #e8f5e9;
        }

        @media (max-width: 768px) {
            .controls {
                flex-direction: column;
                align-items: stretch;
            }

            .filter-buttons {
                flex-direction: column;
            }

            .word-header {
                flex-direction: column;
                align-items: flex-start;
            }
        }
    </style>
</head>
<body>
    <div class="language-popup active" id="languagePopup">
        <div class="popup-content">
            <h2>Select Your Preferred Language</h2>
            <button onclick="selectLanguage('bangla')">বাংলা</button>
            <button onclick="selectLanguage('hindi')">हिंदी</button>
            <button onclick="selectLanguage('japanese')">日本語</button>
        </div>
    </div>

    <div class="header">
        <h1>Magoosh Vocabulary Learning</h1>
    </div>

    <div class="container">
        <div class="controls">
            <div class="filter-buttons">
                <button onclick="filterWords('all')">All Words</button>
                <button onclick="filterWords('memorized')">Memorized</button>
                <button onclick="filterWords('remaining')">Remaining</button>
            </div>
            <button onclick="document.getElementById('languagePopup').classList.add('active')">
                Change Language
            </button>
        </div>

        <div id="wordList"></div>
    </div>

    <script>
        let selectedLanguage = 'bangla';
        let currentFilter = 'all';

        function selectLanguage(language) {
            selectedLanguage = language;
            document.getElementById('languagePopup').classList.remove('active');
            filterWords(currentFilter);
        }

        function filterWords(filter) {
            currentFilter = filter;
            fetch(`/get_words?filter=${filter}`)
                .then(response => response.json())
                .then(words => displayWords(words));
        }

        function toggleMemorized(word) {
            fetch(`/toggle_memorized/${word}`)
                .then(response => response.json())
                .then(result => {
                    if (result.success) {
                        filterWords(currentFilter);
                    }
                });
        }

        function displayWords(words) {
            const wordList = document.getElementById('wordList');
            wordList.innerHTML = '';

            words.forEach(word => {
                const meaningKey = `${selectedLanguage}_meaning`;
                const card = document.createElement('div');
                card.className = `word-card ${word.memorized ? 'memorized' : ''}`;
                
                card.innerHTML = `
                    <div class="word-header">
                        <div>
                            <span class="word-title">${word.word}</span>
                            <span class="word-type">${word.type}</span>
                        </div>
                        <button onclick="toggleMemorized('${word.word}')">
                            ${word.memorized ? 'Unmark' : 'Mark'} as Memorized
                        </button>
                    </div>
                    <div class="meanings">
                        <div class="meaning">
                            <strong>English:</strong> ${word.english_meaning}
                        </div>
                        <div class="meaning">
                            <strong>${selectedLanguage.charAt(0).toUpperCase() + selectedLanguage.slice(1)}:</strong>
                            ${word[meaningKey]}
                        </div>
                    </div>
                    <div class="example">${word.example}</div>
                `;
                
                wordList.appendChild(card);
            });
        }

        // Initial load
        filterWords('all');
    </script>
</body>
</html>
"""

# Write template to file
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(template)

if __name__ == '__main__':
    app.run(debug=True)