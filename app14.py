from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Create a template file instead of using a string
def create_template():
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Magoosh Vocabulary Learning</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <script src="https://code.responsivevoice.org/responsivevoice.js?key=DEMO_KEY"></script>
    <script src="https://code.responsivevoice.org/responsivevoice.js?key=DEMO_KEY"></script>
    <style>
        :root {
            --gradient-start: #4f46e5;
            --gradient-end: #7c3aed;
            --card-size: 280px;
            --gap: 20px;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            min-height: 100vh;
            color: #1e293b;
            padding-bottom: 2rem;
        }

        .header {
            background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
            padding: 2rem;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 1rem;
            position: relative;
        }

        .controls {
            background: white;
            padding: 1rem;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            margin-bottom: 2rem;
            display: flex;
            justify-content: center;
            gap: 1rem;
            flex-wrap: wrap;
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

        /* Card Layout Styles */
        .base-view, .grid-view {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(var(--card-size), 1fr));
            gap: var(--gap);
            padding: var(--gap);
        }

        .list-view {
            display: flex;
            flex-direction: column;
            gap: var(--gap);
            padding: var(--gap);
        }

        .horizontal-scroll-view {
            display: flex;
            overflow-x: auto;
            gap: var(--gap);
            padding: var(--gap);
            scroll-snap-type: x mandatory;
        }

        .masonry-view {
            columns: 4 250px;
            column-gap: var(--gap);
            padding: var(--gap);
        }

        /* Card Styles */
        .word-card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            position: relative;
            min-height: var(--card-size);
            margin-bottom: var(--gap);
            break-inside: avoid;
        }

        .word-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }

        .word-card.expanded {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 90%;
            max-width: 600px;
            height: auto;
            max-height: 90vh;
            overflow-y: auto;
            z-index: 1000;
            min-height: auto;
            animation: expandCard 0.3s ease-out forwards;
        }

        .word-card.memorized {
            background: linear-gradient(145deg, #ecfdf5 0%, #d1fae5 100%);
        }

        .word-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }

        .word-info {
            flex: 1;
        }

        .word-title {
            font-size: 1.4rem;
            color: var(--gradient-start);
            font-weight: 600;
            margin-bottom: 0.3rem;
        }

        .word-type {
            color: #64748b;
            font-size: 0.9rem;
            font-style: italic;
        }

        .word-actions {
            display: flex;
            gap: 0.5rem;
            margin-left: 1rem;
        }

        .sound-button, .star-button {
            background: none;
            border: none;
            cursor: pointer;
            font-size: 1.2rem;
            color: #64748b;
            transition: all 0.3s ease;
            padding: 0.5rem;
        }

        .sound-button:hover, .star-button:hover {
            color: var(--gradient-start);
            transform: scale(1.1);
        }

        .sound-button.speaking {
            color: var(--gradient-start);
            animation: pulse 1s infinite;
        }

        .star-button.memorized {
            color: #fbbf24;
        }

        .meanings {
            margin-top: 1rem;
        }

        .meaning {
            margin: 0.8rem 0;
            line-height: 1.5;
        }

        .meaning strong {
            color: var(--gradient-start);
            font-size: 0.9rem;
            display: block;
            margin-bottom: 0.3rem;
        }

        .examples {
            display: none;
            margin-top: 1.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid #e2e8f0;
        }

        .example {
            margin: 1rem 0;
            padding: 1rem;
            background: #f8fafc;
            border-radius: 8px;
            border-left: 3px solid var(--gradient-start);
        }

        .example strong {
            color: var(--gradient-start);
            display: block;
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
        }

        /* Overlay */
        .overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(4px);
            z-index: 999;
        }

        .overlay.active {
            display: block;
        }

        /* Popup Styles */
        .popup {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(4px);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }

        .popup.active {
            display: flex;
        }

        .popup-content {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            max-width: 90%;
            width: 400px;
        }

        .popup-content h2 {
            text-align: center;
            color: var(--gradient-start);
            margin-bottom: 1.5rem;
        }

        /* Animations */
        @keyframes expandCard {
            from {
                transform: translate(-50%, -50%) scale(0.8);
                opacity: 0;
            }
            to {
                transform: translate(-50%, -50%) scale(1);
                opacity: 1;
            }
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .controls {
                flex-direction: column;
            }

            :root {
                --card-size: 200px;
            }

            .masonry-view {
                columns: 2;
            }

            .word-card.expanded {
                width: 95%;
                max-height: 85vh;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Magoosh Vocabulary Learning</h1>
    </div>

    <div class="container">
        <div class="controls">
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
            <button onclick="showLanguagePopup()" class="filter-button">
                <i class="fas fa-language"></i>
                Change Language
            </button>
            <button onclick="showViewPopup()" class="filter-button">
                <i class="fas fa-th"></i>
                Change View
            </button>
        </div>

        <div id="wordList" class="base-view"></div>
    </div>

    <div class="overlay" id="cardOverlay"></div>

    <div class="popup" id="languagePopup">
        <div class="popup-content">
            <h2>Select Language</h2>
            <div class="controls">
                <button onclick="selectLanguage('bangla')" class="filter-button">বাংলা</button>
                <button onclick="selectLanguage('hindi')" class="filter-button">हिंदी</button>
                <button onclick="selectLanguage('japanese')" class="filter-button">日本語</button>
            </div>
        </div>
    </div>

    <div class="popup" id="viewPopup">
        <div class="popup-content">
            <h2>Select View</h2>
            <div class="controls">
                <button onclick="selectView('base')" class="filter-button">
                    <i class="fas fa-th-large"></i> Base View
                </button>
                <button onclick="selectView('grid')" class="filter-button">
                    <i class="fas fa-th"></i> Grid View
                </button>
                <button onclick="selectView('list')" class="filter-button">
                    <i class="fas fa-list"></i> List View
                </button>
                <button onclick="selectView('horizontal-scroll')" class="filter-button">
                    <i class="fas fa-arrow-right"></i> Horizontal View
                </button>
                <button onclick="selectView('masonry')" class="filter-button">
                    <i class="fas fa-boxes"></i> Masonry View
                </button>
            </div>
        </div>
    </div>
    <script>
        let selectedLanguage = 'bangla';
        let currentView = 'base';
        let expandedCard = null;

        function updateWordCounts(counts) {
            document.getElementById('allCount').textContent = counts.total;
            document.getElementById('memorizedCount').textContent = counts.memorized;
            document.getElementById('remainingCount').textContent = counts.remaining;
        }

        function showLanguagePopup() {
            document.getElementById('languagePopup').classList.add('active');
        }

        function showViewPopup() {
            document.getElementById('viewPopup').classList.add('active');
        }

        function selectLanguage(language) {
            selectedLanguage = language;
            document.getElementById('languagePopup').classList.remove('active');
            filterWords('all');
        }

        function selectView(view) {
            currentView = view;
            document.getElementById('viewPopup').classList.remove('active');
            const wordList = document.getElementById('wordList');
            wordList.className = `${view}-view`;
            filterWords('all');
        }

        function speakWord(event, word, type, meaning) {
    event.stopPropagation();
    const button = event.currentTarget;
    
    // If already speaking, stop it
    if (window.responsiveVoice && window.responsiveVoice.isPlaying()) {
        window.responsiveVoice.cancel();
        button.classList.remove('speaking');
        return;
    }

    // Remove speaking class from all buttons
    document.querySelectorAll('.sound-button').forEach(btn => {
        btn.classList.remove('speaking');
    });

    // Add speaking class to current button
    button.classList.add('speaking');

    // Create text to speak
    const textToSpeak = `${word}. ${type}. ${meaning}`;

    // Use the free voice
    if (window.responsiveVoice) {
        window.responsiveVoice.speak(textToSpeak, "UK English Male", {
            pitch: 1,
            rate: 0.9,
            volume: 1,
            onend: () => button.classList.remove('speaking'),
            onerror: () => button.classList.remove('speaking')
        });
    }
}
        function toggleMemorized(event, word) {
            event.stopPropagation();
            fetch(`/toggle_memorized/${word}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        filterWords('all');
                    }
                });
        }

        function closeExpandedCard() {
            if (expandedCard) {
                expandedCard.classList.remove('expanded');
                expandedCard.querySelector('.examples').style.display = 'none';
                document.getElementById('cardOverlay').classList.remove('active');
                expandedCard = null;
            }
        }

        function toggleCard(card) {
            if (expandedCard === card) {
                closeExpandedCard();
            } else {
                if (expandedCard) {
                    closeExpandedCard();
                }
                card.classList.add('expanded');
                card.querySelector('.examples').style.display = 'block';
                document.getElementById('cardOverlay').classList.add('active');
                expandedCard = card;
            }
        }

        function displayWords(words) {
            const wordList = document.getElementById('wordList');
            wordList.innerHTML = '';

            words.forEach(word => {
                const meaningKey = `${selectedLanguage}_meaning`;
                const exampleKey = `example_${selectedLanguage}`;
                
                const card = document.createElement('div');
                card.className = `word-card ${word.memorized ? 'memorized' : ''}`;
                
                const escapedWord = word.word.replace(/'/g, "\\'");
                const escapedType = word.type.replace(/'/g, "\\'");
                const escapedMeaning = word.english_meaning.replace(/'/g, "\\'");
                
                card.innerHTML = `
                    <div class="word-header">
                        <div class="word-info">
                            <div class="word-title">${word.word}</div>
                            <div class="word-type">${word.type}</div>
                        </div>
                        <div class="word-actions">
                            <button class="sound-button" 
                                    onclick="speakWord(event, '${escapedWord}', '${escapedType}', '${escapedMeaning}')">
                                <i class="fas fa-volume-up"></i>
                            </button>
                            <button class="star-button ${word.memorized ? 'memorized' : ''}" 
                                    onclick="toggleMemorized(event, '${escapedWord}')">
                                <i class="fas fa-star"></i>
                            </button>
                        </div>
                    </div>
                    
                    <div class="meanings">
                        <div class="meaning">
                            <strong>English:</strong>
                            <span>${word.english_meaning}</span>
                        </div>
                        <div class="meaning">
                            <strong>${selectedLanguage.charAt(0).toUpperCase() + selectedLanguage.slice(1)}:</strong>
                            <span>${word[meaningKey]}</span>
                        </div>
                    </div>
                    
                    <div class="examples">
                        <div class="example">
                            <strong>English Example:</strong>
                            <p>${word.example}</p>
                        </div>
                        <div class="example">
                            <strong>${selectedLanguage.charAt(0).toUpperCase() + selectedLanguage.slice(1)} Example:</strong>
                            <p>${word[exampleKey]}</p>
                        </div>
                    </div>
                `;
                
                card.onclick = () => toggleCard(card);
                wordList.appendChild(card);
            });
        }

        function filterWords(filter) {
            fetch(`/get_words?filter=${filter}`)
                .then(response => response.json())
                .then(data => {
                    displayWords(data.words);
                    updateWordCounts(data.counts);
                });
        }

        // Event Listeners
        document.getElementById('cardOverlay').addEventListener('click', closeExpandedCard);

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeExpandedCard();
            }
        });

        // Close popups when clicking outside
        document.addEventListener('click', (event) => {
            if (event.target.classList.contains('popup')) {
                event.target.classList.remove('active');
            }
        });

        // Initial load
        filterWords('all');
    </script>
</body>
</html>'''
    
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

# Sample word data
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
    filtered_words = words
    if filter_type == 'memorized':
        filtered_words = [word for word in words if word['memorized']]
    elif filter_type == 'remaining':
        filtered_words = [word for word in words if not word['memorized']]
    
    return jsonify({
        "words": filtered_words,
        "counts": {
            "total": len(words),
            "memorized": len([w for w in words if w['memorized']]),
            "remaining": len([w for w in words if not w['memorized']])
        }
    })

@app.route('/toggle_memorized/<word>')
def toggle_memorized(word):
    for w in words:
        if w['word'] == word:
            w['memorized'] = not w['memorized']
            return jsonify({
                'success': True,
                'counts': {
                    "total": len(words),
                    "memorized": len([w for w in words if w['memorized']]),
                    "remaining": len([w for w in words if not w['memorized']])
                }
            })
    return jsonify({'success': False})

if __name__ == '__main__':
    create_template()
    app.run(debug=True)