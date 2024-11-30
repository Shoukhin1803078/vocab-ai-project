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
            --gradient-start: #6366f1;
            --gradient-end: #8b5cf6;
            --card-gradient-start: #f8fafc;
            --card-gradient-end: #f1f5f9;
            --text-color: #1e293b;
            --border-color: #e2e8f0;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            color: var(--text-color);
            line-height: 1.6;
            min-height: 100vh;
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
            backdrop-filter: blur(5px);
        }

        .language-popup.active {
            display: flex;
        }

        .popup-content {
            background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            max-width: 90%;
            width: 400px;
            text-align: center;
        }

        .header {
            background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
            color: white;
            padding: 2rem 1rem;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 1rem;
        }

        .controls {
            background: white;
            padding: 1rem;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            margin-bottom: 2rem;
        }

        .filter-buttons {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            justify-content: center;
        }

        .filter-button {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
            color: white;
            transition: all 0.3s ease;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .filter-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
        }

        .word-count {
            background: rgba(255, 255, 255, 0.2);
            padding: 0.2rem 0.6rem;
            border-radius: 20px;
            font-size: 0.9rem;
        }

        .word-card {
            background: linear-gradient(145deg, var(--card-gradient-start), var(--card-gradient-end));
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid var(--border-color);
        }

        .word-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }

        .word-card.expanded {
            background: white;
        }

        .word-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }

        .word-title {
            font-size: 1.5rem;
            color: var(--gradient-start);
            font-weight: 600;
        }

        .word-type {
            color: #64748b;
            font-style: italic;
            font-size: 0.9rem;
        }

        .meanings {
            margin-top: 1rem;
        }

        .meaning {
            margin: 0.5rem 0;
            padding: 0.5rem;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.5);
        }

        .meaning strong {
            color: var(--gradient-start);
            margin-right: 0.5rem;
        }

        .examples {
            display: none;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border-color);
        }

        .example {
            margin: 1rem 0;
            padding: 1rem;
            background: linear-gradient(145deg, #f8fafc 0%, #f1f5f9 100%);
            border-radius: 10px;
            border-left: 4px solid var(--gradient-start);
        }

        .example strong {
            display: block;
            margin-bottom: 0.5rem;
            color: var(--gradient-start);
        }

        .memorize-button {
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
            color: white;
            transition: all 0.3s ease;
            font-weight: 500;
        }

        .memorize-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
        }

        .memorized {
            background: linear-gradient(145deg, #ecfdf5 0%, #d1fae5 100%);
        }

        @media (max-width: 768px) {
            .filter-buttons {
                flex-direction: column;
            }

            .word-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 1rem;
            }
        }
    </style>
</head>
<body>
    <div class="language-popup active" id="languagePopup">
        <div class="popup-content">
            <h2>Select Your Learning Language</h2>
            <button onclick="selectLanguage('bangla')" class="filter-button">
                <span>বাংলা (Bengali)</span>
            </button>
            <button onclick="selectLanguage('hindi')" class="filter-button">
                <span>हिंदी (Hindi)</span>
            </button>
            <button onclick="selectLanguage('japanese')" class="filter-button">
                <span>日本語 (Japanese)</span>
            </button>
        </div>
    </div>

    <div class="header">
        <h1>Magoosh Vocabulary Learning</h1>
    </div>

    <div class="container">
        <div class="controls">
            <div class="filter-buttons">
                <button onclick="filterWords('all')" class="filter-button">
                    <span>All Words</span>
                    <span id="allCount" class="word-count">0</span>
                </button>
                <button onclick="filterWords('memorized')" class="filter-button">
                    <span>Memorized</span>
                    <span id="memorizedCount" class="word-count">0</span>
                </button>
                <button onclick="filterWords('remaining')" class="filter-button">
                    <span>Remaining</span>
                    <span id="remainingCount" class="word-count">0</span>
                </button>
                <button onclick="document.getElementById('languagePopup').classList.add('active')" class="filter-button">
                    Change Language
                </button>
            </div>
        </div>

        <div id="wordList"></div>
    </div>

    <script>
        let selectedLanguage = 'bangla';
        let currentFilter = 'all';
        let expandedCard = null;

        function updateWordCounts(words) {
            const memorizedCount = words.filter(w => w.memorized).length;
            const totalCount = words.length;
            const remainingCount = totalCount - memorizedCount;

            document.getElementById('allCount').textContent = totalCount;
            document.getElementById('memorizedCount').textContent = memorizedCount;
            document.getElementById('remainingCount').textContent = remainingCount;
        }

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
            expandedCard = null;
            fetch(`/get_words?filter=${filter}`)
                .then(response => response.json())
                .then(words => {
                    displayWords(words);
                    updateWordCounts(words);
                });
        }

        function toggleMemorized(event, word) {
            event.stopPropagation();
            fetch(`/toggle_memorized/${word}`)
                .then(response => response.json())
                .then(result => {
                    if (result.success) {
                        filterWords(currentFilter);
                    }
                });
        }

        function toggleCard(card) {
            if (expandedCard && expandedCard !== card) {
                expandedCard.classList.remove('expanded');
                expandedCard.querySelector('.examples').style.display = 'none';
            }

            const examplesSection = card.querySelector('.examples');
            const isExpanded = card.classList.toggle('expanded');
            examplesSection.style.display = isExpanded ? 'block' : 'none';
            expandedCard = isExpanded ? card : null;
        }

        function displayWords(words) {
            const wordList = document.getElementById('wordList');
            wordList.innerHTML = '';

            words.forEach(word => {
                const meaningKey = `${selectedLanguage}_meaning`;
                const exampleKey = `example_${selectedLanguage}`;
                const card = document.createElement('div');
                card.className = `word-card ${word.memorized ? 'memorized' : ''}`;
                card.onclick = () => toggleCard(card);
                
                card.innerHTML = `
                    <div class="word-header">
                        <div>
                            <span class="word-title">${word.word}</span>
                            <span class="word-type">(${word.type})</span>
                        </div>
                        <button class="memorize-button" onclick="toggleMemorized(event, '${word.word}')">
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
        fetch('/get_words')
            .then(response => response.json())
            .then(words => {
                displayWords(words);
                updateWordCounts(words);
            });
    </script>
</body>
</html>
"""

# Write template to file
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(template)

if __name__ == '__main__':
    app.run(debug=True)