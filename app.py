from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import openai
import os
from gtts import gTTS
import uuid

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    prompt = f"""
    أنت شخصية جزائرية عجوز مرحة اسمها "حبيبة وتكرتوش"، عندك 68 سنة، تحبي تضحكي وتردي بنصائح وطرائف.
    جاوب باللهجة الجزائرية، بطريقة مضحكة ومرحة مثل جداتنا، واستعملي تعابير شعبية كيما "يا وليدي"، "وش راك؟"، "آه يا زمان".
    سؤالي: {message}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        reply = response.choices[0].message.content.strip()

        # تحويل إلى صوت باللهجة الجزائرية (نستخدم gTTS للدارجة)
        tts = gTTS(reply, lang='ar')
        audio_filename = f"audio_{uuid.uuid4().hex}.mp3"
        audio_path = os.path.join("static/audio", audio_filename)
        tts.save(audio_path)

        return jsonify({"reply": reply, "audio": audio_filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/audio/<filename>")
def audio(filename):
    return send_from_directory("static/audio", filename).

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)