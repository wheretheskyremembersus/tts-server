from flask import Flask, request, send_file, jsonify
from TTS.api import TTS
import tempfile

app = Flask(__name__)

print("Loading TTS models...")

tts = TTS(model_name="tts_models/en/vctk/vits")

print("Models loaded!")

@app.route("/")
def home():
    return "TTS Server Running"

@app.route("/speak", methods=["POST"])
def speak():
    try:
        data = request.json
        text = data.get("text", "")
        voice = data.get("voice", "ayaan")

        if not text:
            return jsonify({"error": "No text provided"}), 400

        if voice == "saira":
            speaker = "p225"
        else:
            speaker = "p226"

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_path = temp_file.name
        temp_file.close()

        tts.tts_to_file(text=text, speaker=speaker, file_path=temp_path)

        return send_file(temp_path, mimetype="audio/wav")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
