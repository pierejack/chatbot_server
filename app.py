from flask import Flask, request, jsonify, send_from_directory
import openai
from gtts import gTTS
import os
import uuid

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
AUDIO_DIR = "static"
os.makedirs(AUDIO_DIR, exist_ok=True)

@app.route('/chat', methods=['POST'])
def chat():
    user_text = request.json.get("message")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "أنت عجوز جزائرية عندها 68 سنة، إسمك حبيبة وتكرتوش، عندك حس الدعابة، وتتكلمي باللهجة الجزائرية، جاوبي بطريقة ضاحكة وممتعة."},
            {"role": "user", "content": user_text}
        ]
    )
    bot_text = response['choices'][0]['message']['content']

    tts = gTTS(bot_text, lang='ar')
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)
    tts.save(filepath)

    return jsonify({"text": bot_text, "audio": filename})

@app.route('/audio/<filename>', methods=['GET'])
def get_audio(filename):
    return send_from_directory(AUDIO_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
