from flask import Flask, render_template_string, request
from gtts import gTTS
import os

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Text to Speech Card</title>
    <style>
        .card {
            width: 300px;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            position: relative;
            font-family: Arial, sans-serif;
        }
        .card h1 {
            margin: 0 0 10px 0;
            font-size: 18px;
        }
        .card p {
            margin: 0;
            font-size: 14px;
        }
        .sound-button {
            position: absolute;
            top: 10px;
            right: 10px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            cursor: pointer;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <div class="card">
        <button class="sound-button" id="soundButton">🔊</button>
        <h1 id="cardTitle">Sample Heading</h1>
        <p id="cardContent">This is some sample content to demonstrate the text-to-speech functionality.</p>
    </div>

    <script>
        const soundButton = document.getElementById('soundButton');
        const title = document.getElementById('cardTitle').innerText;
        const content = document.getElementById('cardContent').innerText;

        soundButton.addEventListener('click', async function () {
            const response = await fetch('/speak', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: `${title} ${content}` }),
            });

            if (response.ok) {
                const audioBlob = await response.blob();
                const audioUrl = URL.createObjectURL(audioBlob);
                const audio = new Audio(audioUrl);
                audio.play();
            } else {
                alert('Something went wrong. Please try again.');
            }
        });
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_CODE)

@app.route('/speak', methods=['POST'])
def speak():
    from flask import jsonify, request

    data = request.get_json()
    text = data.get('text', '')

    if not text.strip():
        return jsonify({"error": "No text provided"}), 400

    # Generate speech from text
    tts = gTTS(text)
    audio_file = "output.mp3"
    tts.save(audio_file)

    # Send the audio file as a response
    def generate_audio():
        with open(audio_file, 'rb') as f:
            data = f.read()
            yield data
        os.remove(audio_file)  # Clean up the file after sending

    return app.response_class(generate_audio(), mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(debug=True)
