from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from gtts import gTTS
import openai
import os
import uuid

# إعداد التطبيق
app = Flask(__name__)
CORS(app)

# مفتاح OpenAI - تأكد أنك وضعته في بيئة التشغيل على Render
openai.api_key = os.getenv("OPENAI_API_KEY")

# إنشاء مجلد الصوت إن لم يكن موجودًا
os.makedirs("static/audio", exist_ok=True)

# الصفحة الرئيسية (اختياري)
@app.route("/")
def index():
    return "<h2>Chatbot Server is Running</h2>"

# نقطة المحادثة مع البوت
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message")

        if not message:
            return jsonify({"error": "الرسالة غير موجودة"}), 400

        # استجابة GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي يتحدث العربية."},
                {"role": "user", "content": message}
            ]
        )

        reply = response["choices"][0]["message"]["content"]

        # تحويل الرد إلى صوت
        filename = f"{uuid.uuid4()}.mp3"
        audio_path = os.path.join("static/audio", filename)

        try:
            tts = gTTS(text=reply, lang="ar")
            tts.save(audio_path)
        except Exception as e:
            print("gTTS error:", e)
            return jsonify({"error": "فشل في تحويل الرد إلى صوت."}), 500

        return jsonify({"reply": reply, "audio": f"/audio/{filename}"})
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "حدث خطأ في الخادم."}), 500

# تقديم ملفات الصوت عند الطلب
@app.route("/audio/<filename>")
def audio(filename):
    return send_from_directory("static/audio", filename)

# تشغيل التطبيق على Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=False, host="0.0.0.0", port=port)
