from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import openai
from gtts import gTTS
import os
import uuid

app = Flask(__name__)
CORS(app)

# تأكد أنك تضع مفتاحك هنا
openai.api_key = "YOUR_OPENAI_API_KEY"

# مجلد لحفظ الملفات الصوتية
AUDIO_FOLDER = "static/audio"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "الخادم يعمل بنجاح. اذهب إلى الواجهة الأمامية للتحدث مع البوت."

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "").strip()
        
        if not message:
            return jsonify({"error": "الرسالة فارغة"}), 400

        # استدعاء ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # أو gpt-4 حسب المتاح
            messages=[
                {"role": "system", "content": "أنت مساعد ودود وذكي."},
                {"role": "user", "content": message}
            ]
        )

        reply = response["choices"][0]["message"]["content"]

        # تحويل الرد إلى صوت
        tts = gTTS(text=reply, lang="ar")
        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join(AUDIO_FOLDER, filename)
        tts.save(filepath)

        return jsonify({
            "reply": reply,
            "audio_url": f"/audio/{filename}"
        })

    except Exception as e:
        print("حدث خطأ:", e)
        return jsonify({"error": "حدث خطأ في الخادم."}), 500

@app.route("/audio/<filename>")
def audio(filename):
    return send_from_directory(AUDIO_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
