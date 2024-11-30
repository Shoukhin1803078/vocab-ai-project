from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

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
    },
    {
        "word": "abstruse",
        "type": "adjective",
        "english_meaning": "difficult to understand; obscure",
        "bangla_meaning": "দুর্বোধ্য",
        "hindi_meaning": "दुर्बोध",
        "japanese_meaning": "難解な",
        "example": "The professor's abstruse explanation left many students confused.",
        "example_bangla": "অধ্যাপকের দুর্বোধ্য ব্যাখ্যা অনেক শিক্ষার্থীকে বিভ্রান্ত করে তুলল।",
        "example_hindi": "प्रोफेसर की दुर्बोध व्याख्या ने कई छात्रों को भ्रमित कर दिया।",
        "example_japanese": "教授の難解な説明は多くの学生を混乱させた。",
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
        return jsonify({"words": words, "counts": get_counts()})
    elif filter_type == 'memorized':
        filtered_words = [word for word in words if word['memorized']]
        return jsonify({"words": filtered_words, "counts": get_counts()})
    else:  # remaining
        filtered_words = [word for word in words if not word['memorized']]
        return jsonify({"words": filtered_words, "counts": get_counts()})

def get_counts():
    total = len(words)
    memorized = len([word for word in words if word['memorized']])
    remaining = total - memorized
    return {
        "total": total,
        "memorized": memorized,
        "remaining": remaining
    }

@app.route('/toggle_memorized/<word>')
def toggle_memorized(word):
    for w in words:
        if w['word'] == word:
            w['memorized'] = not w['memorized']
            return jsonify({'success': True, 'counts': get_counts()})
    return jsonify({'success': False})

# HTML template string
template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Magoosh Vocabulary Learning</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <script src="https://code.responsivevoice.org/responsivevoice.js?key=DEMO_KEY"></script>
    <style>
        :root {
            --gradient-start: #4f46e5;
            --gradient-end: #7c3aed;
            --card-size: 220px;
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

        .word-count {
            background: rgba(255, 255, 255, 0.2);
            padding: 0.2rem 0.6rem;
            border-radius: 20px;
            font-size: 0.9rem;
        }

        /* Base View */
        .base-view {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(var(--card-size), 1fr));
            gap: var(--gap);
            padding: var(--gap);
        }

        /* Grid View */
        .grid-view {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(var(--card-size), 1fr));
            gap: var(--gap);
            padding: var(--gap);
        }

        /* List View */
        .list-view {
            display: flex;
            flex-direction: column;
            gap: var(--gap);
            padding: var(--gap);
        }

        .list-view .word-card {
            height: auto;
            min-height: 120px;
        }

        /* Horizontal Scroll View */
        .horizontal-scroll-view {
            display: flex;
            overflow-x: auto;
            gap: var(--gap);
            padding: var(--gap);
            scroll-snap-type: x mandatory;
        }

        .horizontal-scroll-view .word-card {
            flex: 0 0 300px;
            scroll-snap-align: start;
        }

        /* Masonry View */
        .masonry-view {
            columns: 5 200px;
            column-gap: var(--gap);
            padding: var(--gap);
        }

        .masonry-view .word-card {
            break-inside: avoid;
            margin-bottom: var(--gap);
            height: auto;
        }

        /* Carousel View */
        .carousel-view {
            position: relative;
            padding: var(--gap);
        }

        .carousel-container {
            overflow: hidden;
            position: relative;
        }

        .carousel-track {
            display: flex;
            transition: transform 0.5s ease-in-out;
        }

        .carousel-button {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background: white;
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            z-index: 10;
        }

        .carousel-button.prev {
            left: 20px;
        }

        .carousel-button.next {
            right: 20px;
        }

        /* Card Styles */
        .word-card {
            background: white;
            border-radius: 15px;
            min-height: var(--card-size);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }

        .word-card.memorized {
            background: linear-gradient(145deg, #ecfdf5 0%, #d1fae5 100%);
        }

        .card-content {
            padding: 1.5rem;
            height: 100%;
        }

        .word-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }

        .word-info {
            display: flex;
            flex-direction: column;
        }

        .word-title {
            font-size: 1.2rem;
            color: var(--gradient-start);
            font-weight: 600;
            line-height: 1.2;
        }

        .word-type {
            color: #64748b;
            font-size: 0.8rem;
            font-style: italic;
            margin-top: 0.2rem;
        }

        .word-actions {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .sound-button {
            background: none;
            border: none;
            cursor: pointer;
            font-size: 1.5rem;
            color: #64748b;
            transition: all 0.3s ease;
            padding: 0.5rem;
        }

        .sound-button:hover {
            color: var(--gradient-start);
            transform: scale(1.1);
        }

        .sound-button.speaking {
            color: var(--gradient-start);
            animation: pulse 1s infinite;
        }

        .star-button {
            background: none;
            border: none;
            cursor: pointer;
            font-size: 1.5rem;
            color: #cbd5e1;
            transition: all 0.3s ease;
            padding: 0.5rem;
        }

        .star-button.memorized {
            color: #fbbf24;
        }

        .close-button {
            display: none;
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: none;
            border: none;
            color: #64748b;
            cursor: pointer;
            font-size: 1.2rem;
            z-index: 2;
        }

        .word-card.expanded .close-button {
            display: block;
        }

        .meanings {
            font-size: 0.9rem;
        }

        .meaning {
            margin: 0.5rem 0;
        }

        .meaning strong {
            color: var(--gradient-start);
            font-size: 0.8rem;
        }

        .examples {
            display: none;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid #e2e8f0;
        }

        .example {
            margin: 1rem 0;
            font-size: 0.9rem;
            padding: 1rem;
            background: #f8fafc;
            border-radius: 8px;
            border-left: 3px solid var(--gradient-start);
        }

        /* Expanded Card Styles */
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
            aspect-ratio: auto;
        }

        .card-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(5px);
            z-index: 999;
        }

        /* Popup Styles */
        .popup {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(5px);
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
            text-align: center;
        }

        .popup h2 {
            margin-bottom: 1.5rem;
            color: var(--gradient-start);
        }

        .option-buttons {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .option-button {
            width: 100%;
            padding: 1rem;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
            color: white;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            font-size: 1rem;
        }

        .option-button i {
            font-size: 1.2rem;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }

        @keyframes cardExpand {
            from {
                transform: translate(-50%, -50%) scale(0.8);
                opacity: 0;
            }
            to {
                transform: translate(-50%, -50%) scale(1);
                opacity: 1;
            }
        }

        @media (max-width: 768px) {
            .controls {
                flex-direction: column;
            }

            :root {
                --card-size: 160px;
            }

            .masonry-view {
                columns: 2 160px;
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
                Change Language
            </button>
            <button onclick="showViewPopup()" class="filter-button">
                <i class="fas fa-th"></i>
                Change View
            </button>
        </div>

        <div id="wordList" class="base-view"></div>
    </div>

    <div class="card-overlay" id="cardOverlay"></div>

    <div class="popup" id="languagePopup">
        <div class="popup-content">
            <h2>Select Your Learning Language</h2>
            <div class="option-buttons">
                <button onclick="selectLanguage('bangla')" class="option-button">
                    <span class="native-text">বাংলা</span>
                    <span class="english-text">Bengali</span>
                </button>
                <button onclick="selectLanguage('hindi')" class="option-button">
                    <span class="native-text">हिंदी</span>
                    <span class="english-text">Hindi</span>
                </button>
                <button onclick="selectLanguage('japanese')" class="option-button">
                    <span class="native-text">日本語</span>
                    <span class="english-text">Japanese</span>
                </button>
            </div>
        </div>
    </div>

    <div class="popup" id="viewPopup">
        <div class="popup-content">
            <h2>Select View Style</h2>
            <div class="option-buttons">
                <button onclick="selectView('base')" class="option-button">
                    <i class="fas fa-grip-horizontal"></i>
                    Base View
                </button>
                <button onclick="selectView('grid')" class="option-button">
                    <i class="fas fa-th"></i>
                    Grid View
                </button>
                <button onclick="selectView('list')" class="option-button">
                    <i class="fas fa-list"></i>
                    List View
                </button>
                <button onclick="selectView('horizontal-scroll')" class="option-button">
                    <i class="fas fa-arrows-left-right"></i>
                    Horizontal Scroll View
                </button>
                <button onclick="selectView('masonry')" class="option-button">
                    <i class="fas fa-boxes-stacked"></i>
                    Masonry View
                </button>
                <button onclick="selectView('carousel')" class="option-button">
                    <i class="fas fa-images"></i>
                    Carousel View
                </button>
            </div>
        </div>
    </div>

    <script>
        let selectedLanguage = 'bangla';
        let currentFilter = 'all';
        let currentView = 'base';
        let expandedCard = null;
        let carouselIndex = 0;

        function updateWordCounts(counts) {
            document.getElementById('allCount').textContent = counts.total;
            document.getElementById('memorizedCount').textContent = counts.memorized;
            document.getElementById('remainingCount').textContent = counts.remaining;
        }

        function getLanguageLabel(language) {
            const labels = {
                'bangla': 'বাংলা',
                'hindi': 'हिंदी',
                'japanese': '日本語'
            };
            return labels[language] || language;
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
            filterWords(currentFilter);
        }

        function selectView(view) {
            currentView = view;
            document.getElementById('viewPopup').classList.remove('active');
            const wordList = document.getElementById('wordList');
            wordList.className = `${view}-view`;
            filterWords(currentFilter);
        }

        function filterWords(filter) {
            currentFilter = filter;
            closeExpandedCard();
            fetch(`/get_words?filter=${filter}`)
                .then(response => response.json())
                .then(data => {
                    displayWords(data.words);
                    updateWordCounts(data.counts);
                });
        }

        function toggleMemorized(event, word) {
            event.stopPropagation();
            fetch(`/toggle_memorized/${word}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        filterWords(currentFilter);
                    }
                });
        }

        function speakWord(event, word, type, meaning) {
            event.stopPropagation();
            const button = event.currentTarget;
            
            if (responsiveVoice.isPlaying()) {
                responsiveVoice.cancel();
                button.classList.remove('speaking');
                return;
            }

            button.classList.add('speaking');
            const text = `${word}. ${type}. ${meaning}`;
            
            responsiveVoice.speak(text, "UK English Male", {
                onend: () => button.classList.remove('speaking'),
                onerror: () => button.classList.remove('speaking'),
                rate: 0.9,
                pitch: 1
            });
        }

        function closeExpandedCard() {
            if (responsiveVoice.isPlaying()) {
                responsiveVoice.cancel();
                document.querySelectorAll('.sound-button').forEach(btn => {
                    btn.classList.remove('speaking');
                });
            }
            if (expandedCard) {
                expandedCard.classList.remove('expanded');
                expandedCard.querySelector('.examples').style.display = 'none';
                document.getElementById('cardOverlay').style.display = 'none';
                expandedCard = null;
            }
        }

        function toggleCard(card) {
            if (expandedCard === card) {
                closeExpandedCard();
            } else {
                closeExpandedCard();
                card.classList.add('expanded');
                card.querySelector('.examples').style.display = 'block';
                document.getElementById('cardOverlay').style.display = 'block';
                expandedCard = card;
            }
        }

        function moveCarousel(direction) {
            const cards = document.querySelectorAll('.carousel-view .word-card');
            if (cards.length === 0) return;

            if (direction === 'next') {
                carouselIndex = (carouselIndex + 1) % cards.length;
            } else {
                carouselIndex = (carouselIndex - 1 + cards.length) % cards.length;
            }

            const track = document.querySelector('.carousel-track');
            track.style.transform = `translateX(-${carouselIndex * 100}%)`;
        }

        function displayWords(words) {
            const wordList = document.getElementById('wordList');
            wordList.innerHTML = '';

            let container = wordList;
            
            if (currentView === 'carousel') {
                const track = document.createElement('div');
                track.className = 'carousel-track';
                const prevButton = document.createElement('button');
                prevButton.className = 'carousel-button prev';
                prevButton.innerHTML = '<i class="fas fa-chevron-left"></i>';
                prevButton.onclick = (e) => {
                    e.stopPropagation();
                    moveCarousel('prev');
                };
                
                const nextButton = document.createElement('button');
                nextButton.className = 'carousel-button next';
                nextButton.innerHTML = '<i class="fas fa-chevron-right"></i>';
                nextButton.onclick = (e) => {
                    e.stopPropagation();
                    moveCarousel('next');
                };

                wordList.appendChild(prevButton);
                wordList.appendChild(nextButton);
                wordList.appendChild(track);
                container = track;
            }

            words.forEach(word => {
                const meaningKey = `${selectedLanguage}_meaning`;
                const exampleKey = `example_${selectedLanguage}`;
                const card = document.createElement('div');
                card.className = `word-card ${word.memorized ? 'memorized' : ''}`;
                card.onclick = () => toggleCard(card);
                
                card.innerHTML = `
                    <div class="card-content">
                        <button class="close-button" onclick="event.stopPropagation(); closeExpandedCard();">
                            <i class="fas fa-times"></i>
                        </button>
                        <div class="word-header">
                            <div class="word-info">
                                <div class="word-title">${word.word}</div>
                                <div class="word-type">${word.type}</div>
                            </div>
                            <div class="word-actions">
                                <button class="sound-button" 
                                        onclick="speakWord(event, '${word.word}', '${word.type}', '${word.english_meaning}')">
                                    <i class="fas fa-volume-up"></i>
                                </button>
                                <button class="star-button ${word.memorized ? 'memorized' : ''}" 
                                        onclick="toggleMemorized(event, '${word.word}')">
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
                    </div>
                `;
                
                container.appendChild(card);
            });
        }

        document.getElementById('cardOverlay').addEventListener('click', closeExpandedCard);

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeExpandedCard();
            }
        });

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