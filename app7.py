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
        "word": "aberration",
        "type": "noun",
        "english_meaning": "a deviation from what is normal or expected",
        "bangla_meaning": "স্বাভাবিক বা প্রত্যাশিত থেকে বিচ্যুতি",
        "hindi_meaning": "सामान्य या अपेक्षित से विचलन",
        "japanese_meaning": "正常または予想されるものからの逸脱",
        "example": "Aberrations in climate have become the norm: rarely a week goes by without some meteorological phenomenon making headlines.",
        "example_bangla": "জলবায়ুতে বিচ্যুতি এখন স্বাভাবিক হয়ে উঠেছে: কোনো একটি সপ্তাহই যায় না, যেটিতে কিছু না কিছু আবহাওয়া ঘটনা শিরোনাম হয় না।",
        "example_hindi": "जलवायु में विचलन सामान्य हो गया है: शायद ही कोई सप्ताह बिना किसी मौसम संबंधी घटना की सुर्खियां बनाए बीतता है।",
        "example_japanese": "気候の異常は通常のものとなりつつあります：週ごとに気象現象が見出しを飾らないことはほとんどありません。",
        "memorized": False
    },
    {
        "word": "abstain",
        "type": "verb",
        "english_meaning": "choose not to consume or take part in (particularly something enjoyable)",
        "bangla_meaning": "পরিহার করা বা অংশ না নেওয়া (বিশেষত কিছু উপভোগ্য জিনিসে)",
        "hindi_meaning": "कुछ करने से बचना या हिस्सा न लेना (विशेषकर कुछ आनंददायक में)",
        "japanese_meaning": "控える、参加しない（特に楽しめるものについて）",
        "example": "Considered a health nut, Jessica abstained from anything containing sugar--even chocolate.",
        "example_bangla": "স্বাস্থ্য সচেতন হিসেবে পরিচিত, জেসিকা চিনি যুক্ত যে কোনো কিছুই পরিহার করতেন—এমনকি চকোলেটও।",
        "example_hindi": "एक स्वास्थ्य-प्रेमी मानी जाने वाली जेसिका ने चीनी युक्त किसी भी चीज़ से परहेज किया - यहाँ तक कि चॉकलेट भी।",
        "example_japanese": "健康志向と考えられていたジェシカは、砂糖を含むもの、チョコレートさえも控えました。",
        "memorized": False
    },
    {
        "word": "abstruse",
        "type": "adjective",
        "english_meaning": "difficult to understand; incomprehensible",
        "bangla_meaning": "বুঝতে কঠিন; দুর্বোধ্য",
        "hindi_meaning": "समझने में कठिन; अज्ञेय",
        "japanese_meaning": "理解しにくい; 難解な",
        "example": "Physics textbooks can seem so abstruse to the uninitiated that readers feel as though they are looking at hieroglyphics.",
        "example_bangla": "পদার্থবিজ্ঞানের পাঠ্যবইগুলো অজ্ঞদের কাছে এতটাই দুর্বোধ্য বলে মনে হতে পারে যে পাঠকরা যেন হায়ারোগ্লিফিকস দেখছেন বলে মনে করেন।",
        "example_hindi": "भौतिकी की पाठ्यपुस्तकें अज्ञानी लोगों के लिए इतनी कठिन लग सकती हैं कि पाठकों को ऐसा लगे जैसे वे चित्रलिपि देख रहे हों।",
        "example_japanese": "物理学の教科書は初心者には非常に難解に思え、読者はまるでヒエログリフを見ているかのように感じることがあります。",
        "memorized": False
    },
    {
        "word": "accolade",
        "type": "noun",
        "english_meaning": "an award or praise granted as a special honor",
        "bangla_meaning": "একটি পুরস্কার বা প্রশংসা যা বিশেষ সম্মানের জন্য দেওয়া হয়",
        "hindi_meaning": "एक पुरस्कार या प्रशंसा जो विशेष सम्मान के रूप में दी जाती है",
        "japanese_meaning": "特別な名誉として授与される賞または称賛",
        "example": "Jean Paul-Sartre was not a fan of accolades, and as such, he refused to accept the Nobel Prize for Literature in 1964.",
        "example_bangla": "জঁ-পল সার্ত্রে প্রশংসার ভক্ত ছিলেন না, এবং সে কারণে, তিনি ১৯৬৪ সালে সাহিত্যের জন্য নোবেল পুরস্কার গ্রহণ করতে অস্বীকৃতি জানান।",
        "example_hindi": "जीन-पॉल सार्त्र प्रशंसा के प्रशंसक नहीं थे, और इस तरह, उन्होंने 1964 में साहित्य के लिए नोबेल पुरस्कार स्वीकार करने से इनकार कर दिया।",
        "example_japanese": "ジャン・ポール・サルトルは栄誉を好まなかったため、1964年に文学のノーベル賞を受け取ることを拒否しました。",
        "memorized": False
    },
    {
        "word": "acerbic",
        "type": "adjective",
        "english_meaning": "harsh in tone",
        "bangla_meaning": "কঠোর সুরে",
        "hindi_meaning": "कठोर स्वर में",
        "japanese_meaning": "厳しい口調で",
        "example": "Most movie critics are acerbic towards summer blockbusters, often referring to them as garbage.",
        "example_bangla": "বেশিরভাগ চলচ্চিত্র সমালোচক গ্রীষ্মের ব্লকবাস্টারগুলোর প্রতি কঠোর, প্রায়ই এগুলোকে আবর্জনা বলে উল্লেখ করেন।",
        "example_hindi": "अधिकांश फिल्म समीक्षक ग्रीष्मकालीन ब्लॉकबस्टरों के प्रति कठोर होते हैं, अक्सर उन्हें कचरा कहते हैं।",
        "example_japanese": "ほとんどの映画評論家は夏の大ヒット作に対して辛辣で、それらをゴミと呼ぶことがよくあります。",
        "memorized": False
    },
    {
        "word": "acrimony",
        "type": "noun",
        "english_meaning": "bitterness and ill will",
        "bangla_meaning": "তিক্ততা এবং কু-মনের প্রকাশ",
        "hindi_meaning": "कड़वाहट और द्वेष",
        "japanese_meaning": "辛辣さと悪意",
        "example": "The acrimonious dispute between the president and vice-president sent a clear signal to voters: the health of the current administration was imperiled.",
        "example_bangla": "রাষ্ট্রপতি এবং সহ-রাষ্ট্রপতির মধ্যে তিক্ত বিরোধ ভোটারদের কাছে একটি স্পষ্ট সংকেত পাঠিয়েছিল: বর্তমান প্রশাসনের সুস্থতা বিপন্ন।",
        "example_hindi": "राष्ट्रपति और उपराष्ट्रपति के बीच कड़वे विवाद ने मतदाताओं को एक स्पष्ट संकेत दिया: वर्तमान प्रशासन की स्थिति संकट में थी।",
        "example_japanese": "大統領と副大統領の間の辛辣な争いは、有権者に明確な信号を送りました：現在の行政の健全性が危機に瀕していました。",
        "memorized": False
    },
    {
        "word": "adamant",
        "type": "adjective",
        "english_meaning": "refusing to change one's mind",
        "bangla_meaning": "মনের পরিবর্তন করতে অস্বীকার করা",
        "hindi_meaning": "अपना विचार बदलने से इनकार करना",
        "japanese_meaning": "決して譲らない",
        "example": "Civil rights icon Rosa Parks will forever be remembered for adamantly refusing to give up her seat on a public bus--even after the bus driver insisted, she remained rooted in place.",
        "example_bangla": "নাগরিক অধিকার আইকন রোজা পার্কস সর্বদা স্মরণীয় থাকবেন, কারণ তিনি তার স্থান থেকে সরে যেতে অস্বীকার করেছিলেন।",
        "example_hindi": "सिविल राइट्स की आइकन रोज़ा पार्क्स को हमेशा याद किया जाएगा, क्योंकि उन्होंने अपनी सीट छोड़ने से सख्ती से इनकार कर दिया था।",
        "example_japanese": "市民権運動の象徴ローザ・パークスは、バス運転手に要求されても席を譲らなかったことで永遠に記憶されるでしょう。",
        "memorized": False
    },
    {
        "word": "admonish",
        "type": "verb",
        "english_meaning": "to warn strongly, even to the point of reprimanding",
        "bangla_meaning": "কঠোরভাবে সতর্ক করা, প্রয়োজনে তিরস্কার করা",
        "hindi_meaning": "कड़े शब्दों में चेतावनी देना, यहां तक कि डांटने तक",
        "japanese_meaning": "厳しく警告する、時には叱責するまで",
        "example": "Before the concert began, security personnel admonished the crowd not to come up on stage during the performance.",
        "example_bangla": "কনসার্ট শুরুর আগে, নিরাপত্তা কর্মীরা ভিড়কে পারফরম্যান্সের সময় মঞ্চে না আসার জন্য সতর্ক করেছিলেন।",
        "example_hindi": "कॉन्सर्ट शुरू होने से पहले, सुरक्षा कर्मियों ने भीड़ को प्रदर्शन के दौरान मंच पर न आने की चेतावनी दी।",
        "example_japanese": "コンサートが始まる前に、警備員は観客にパフォーマンス中にステージに上がらないよう警告しました。",
        "memorized": False
    },
    {
        "word": "admonitory",
        "type": "adjective",
        "english_meaning": "serving to warn; expressing reproof or reproach especially as a corrective",
        "bangla_meaning": "সতর্ক করার জন্য ব্যবহৃত; সংশোধনের জন্য ধিক্কার প্রকাশ করা",
        "hindi_meaning": "चेतावनी देने वाला; सुधार के लिए निंदा या तिरस्कार व्यक्त करना",
        "japanese_meaning": "警告を示す; 特に是正としての非難を表現する",
        "example": "At the assembly, the high school vice-principal gave the students an admonitory speech, warning them of the many risks and dangers of prom night.",
        "example_bangla": "অ্যাসেম্বলিতে, হাই স্কুলের সহ-প্রধান শিক্ষক শিক্ষার্থীদের প্রম নাইটের বিভিন্ন ঝুঁকি ও বিপদ সম্পর্কে সতর্ক করে একটি সতর্কতামূলক বক্তব্য দেন।",
        "example_hindi": "सभा में, हाई स्कूल के उप-प्राचार्य ने छात्रों को प्रोम नाइट के कई खतरों और जोखिमों के बारे में चेतावनी देते हुए एक चेतावनीपूर्ण भाषण दिया।",
        "example_japanese": "集会で、高校の副校長は、プロムナイトの多くのリスクと危険について警告する説教を生徒に行いました。",
        "memorized": False
    },
    {
        "word": "aesthete",
        "type": "noun",
        "english_meaning": "one who professes great sensitivity to the beauty of art and nature",
        "bangla_meaning": "শিল্প ও প্রকৃতির সৌন্দর্যের প্রতি গভীর সংবেদনশীল ব্যক্তি",
        "hindi_meaning": "कला और प्रकृति की सुंदरता के प्रति गहरी संवेदनशीलता वाला व्यक्ति",
        "japanese_meaning": "芸術と自然の美しさに対する鋭い感性を持つ人",
        "example": "A true aesthete, Marty would spend hours at the Guggenheim Museum, staring at the same Picasso.",
        "example_bangla": "একজন প্রকৃত সৌন্দর্যপ্রেমী হিসেবে, মার্টি গুগেনহাইম যাদুঘরে ঘণ্টার পর ঘণ্টা কাটাতেন, একই পিকাসোর দিকে তাকিয়ে।",
        "example_hindi": "एक सच्चे सौंदर्यप्रेमी, मार्टी गगनहेम संग्रहालय में घंटों बिताते थे, एक ही पिकासो को देखते हुए।",
        "example_japanese": "真の審美家であるマーティは、グッゲンハイム美術館で同じピカソを見つめながら何時間も過ごしました。",
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
    <style>
        :root {
            --gradient-start: #4f46e5;
            --gradient-end: #7c3aed;
            --card-size: 200px;
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

        /* Base Word Card Styles */
        .word-card {
            background: white;
            border-radius: 15px;
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

        /* Grid View */
        .grid-view {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(var(--card-size), 1fr));
            gap: var(--gap);
            padding: var(--gap);
        }

        .grid-view .word-card {
            aspect-ratio: 1;
            height: var(--card-size);
        }

        /* List View */
        .list-view {
            display: flex;
            flex-direction: column;
            gap: var(--gap);
            padding: var(--gap);
        }

        .list-view .word-card {
            width: 100%;
        }

        /* Horizontal Scroll View */
        .horizontal-scroll-view {
            display: flex;
            overflow-x: auto;
            gap: var(--gap);
            padding: var(--gap);
            scroll-snap-type: x mandatory;
            scrollbar-width: thin;
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

        .carousel-view .word-card {
            flex: 0 0 100%;
            max-width: 600px;
            margin: 0 auto;
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

        .word-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }

        .word-title {
            font-size: 1.2rem;
            color: var(--gradient-start);
            font-weight: 600;
            margin-bottom: 0.3rem;
        }

        .word-type {
            color: #64748b;
            font-size: 0.8rem;
            font-style: italic;
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
            gap: 0.5rem;
        }

        .option-button i {
            font-size: 1.2rem;
        }

        .option-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
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

        .word-card.expanded {
            animation: cardExpand 0.3s ease-out forwards;
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

        <div id="wordList" class="grid-view"></div>
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
        let currentView = 'grid';
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

        function closeExpandedCard() {
            if (expandedCard) {
                expandedCard.classList.remove('expanded');
                expandedCard.querySelector('.examples').style.display = 'none';
                expandedCard.querySelector('.close-button').style.display = 'none';
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
                card.querySelector('.close-button').style.display = 'block';
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

            if (currentView === 'carousel') {
                const track = document.createElement('div');
                track.className = 'carousel-track';
                const prevButton = document.createElement('button');
                prevButton.className = 'carousel-button prev';
                prevButton.innerHTML = '<i class="fas fa-chevron-left"></i>';
                prevButton.onclick = () => moveCarousel('prev');
                
                const nextButton = document.createElement('button');
                nextButton.className = 'carousel-button next';
                nextButton.innerHTML = '<i class="fas fa-chevron-right"></i>';
                nextButton.onclick = () => moveCarousel('next');

                wordList.appendChild(prevButton);
                wordList.appendChild(nextButton);
                wordList.appendChild(track);
                wordList = track;
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
                            <div>
                                <div class="word-title">${word.word}</div>
                                <div class="word-type">${word.type}</div>
                            </div>
                            <button class="star-button ${word.memorized ? 'memorized' : ''}" 
                                    onclick="toggleMemorized(event, '${word.word}')">
                                <i class="fas fa-star"></i>
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
                    </div>
                `;
                
                wordList.appendChild(card);
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