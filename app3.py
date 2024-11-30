from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

# Sample word data - you can expand this with your full word list
words = [
    {
        "word": "aberrant",
        "type": "adjective",
        "english_meaning": "markedly different from an accepted norm",
        "bangla_meaning": "স্বাভাবিক থেকে ব্যতিক্রম",
        "hindi_meaning": "असामान्य, विचलित",
        "japanese_meaning": "異常な",
        "example": "When the financial director started screaming and throwing food at his co-workers, the police had to come in to deal with his aberrant behavior.",
        "example_bangla": "যখন আর্থিক পরিচালক চিৎকার করতে শুরু করলেন এবং তার সহকর্মীদের দিকে খাবার ছুড়তে শুরু করলেন, পুলিশকে তার অস্বাভাবিক আচরণ সামলাতে আসতে হয়েছিল।",
        "example_hindi": "जब वित्तीय निदेशक चिल्लाने लगा और अपने सहकर्मियों पर खाना फेंकने लगा, तब पुलिस को उसके असामान्य व्यवहार से निपटने के लिए आना पड़ा।",
        "example_japanese": "財務担当取締役が叫び始め、同僚に食べ物を投げつけ始めたとき、警察は彼の異常な行動に対処するために介入しなければならなかった。",
        "memorized": False
    }
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
        :root {
            --primary-color: #4a90e2;
            --secondary-color: #f5f5f5;
            --text-color: #333;
            --border-color: #e1e4e8;
            --hover-color: #357abd;
            --memorized-color: #e8f5e9;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f2f5;
            color: var(--text-color);
            line-height: 1.6;
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
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
            max-width: 90%;
            width: 400px;
            text-align: center;
        }

        .language-description {
            margin: 1rem 0 1.5rem;
            color: #666;
        }

        .language-button {
            width: 100%;
            margin: 0.8rem 0;
            padding: 1rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.5rem;
        }

        .native-text {
            font-size: 1.2rem;
            font-weight: 500;
        }

        .english-text {
            font-size: 0.9rem;
            opacity: 0.8;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 1rem;
        }

        .header {
            background-color: var(--primary-color);
            color: white;
            padding: 1.5rem;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
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
            transition: all 0.3s ease;
        }

        button:hover {
            background-color: var(--hover-color);
        }

        .word-card {
            background-color: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            transition: transform 0.3s ease;
        }

        .word-card:hover {
            transform: translateY(-3px);
        }

        .word-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border-color);
        }

        .word-title {
            font-size: 1.75rem;
            color: var(--primary-color);
            font-weight: 600;
            margin-right: 0.5rem;
        }

        .word-type {
            color: #666;
            font-style: italic;
        }

        .meanings {
            margin: 1rem 0;
            padding: 1rem;
            background-color: var(--secondary-color);
            border-radius: 8px;
        }

        .meaning {
            margin: 0.5rem 0;
        }

        .meaning strong {
            color: var(--primary-color);
            margin-right: 0.5rem;
        }

        .examples {
            margin-top: 1rem;
        }

        .example {
            margin: 1rem 0;
            padding: 1rem;
            border-left: 4px solid var(--primary-color);
            background-color: var(--secondary-color);
            border-radius: 0 8px 8px 0;
        }

        .example strong {
            display: block;
            margin-bottom: 0.5rem;
            color: var(--primary-color);
        }

        .example p {
            margin: 0.5rem 0;
            line-height: 1.6;
        }

        .memorized {
            background-color: var(--memorized-color);
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
                gap: 1rem;
            }

            .word-header button {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="language-popup active" id="languagePopup">
        <div class="popup-content">
            <h2>Select Your Learning Language</h2>
            <div class="language-description">Choose the language you want to learn vocabulary in:</div>
            <button onclick="selectLanguage('bangla')" class="language-button">
                <span class="native-text">বাংলা</span>
                <span class="english-text">Bengali</span>
            </button>
            <button onclick="selectLanguage('hindi')" class="language-button">
                <span class="native-text">हिंदी</span>
                <span class="english-text">Hindi</span>
            </button>
            <button onclick="selectLanguage('japanese')" class="language-button">
                <span class="native-text">日本語</span>
                <span class="english-text">Japanese</span>
            </button>
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

        function getLanguageLabel(language) {
            const labels = {
                'bangla': 'বাংলা',
                'hindi': 'हिंदी',
                'japanese': '日本語'
            };
            return labels[language] || language;
        }

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
                const exampleKey = `example_${selectedLanguage}`;
                const card = document.createElement('div');
                card.className = `word-card ${word.memorized ? 'memorized' : ''}`;
                
                card.innerHTML = `
                    <div class="word-header">
                        <div>
                            <span class="word-title">${word.word}</span>
                            <span class="word-type">(${word.type})</span>
                        </div>
                        <button onclick="toggleMemorized('${word.word}')">
                            ${word.memorized ? 'Unmark' : 'Mark'} as Memorized
                        </button>
                    </div>
                    
                    <div class="meanings">
                        <div class="meaning">
                            <strong>English:</strong> 
                            <span>${word.english_meaning}</span>
                        </div>
                        <div class="meaning">
                            <strong>${getLanguageLabel(selectedLanguage)}:</strong>
                            <span>${word[meaningKey]}</span>
                        </div>
                    </div>
                    
                    <div class="examples">
                        <div class="example">
                            <strong>English Example:</strong>
                            <p>${word.example}</p>
                        </div>
                        <div class="example">
                            <strong>${getLanguageLabel(selectedLanguage)} Example:</strong>
                            <p>${word[exampleKey]}</p>
                        </div>
                    </div>
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