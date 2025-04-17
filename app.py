import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()  # .env 불러오기

app = Flask(__name__)

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

# Slack 메시지 보내기
def send_slack_message(channel, text):
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "channel": channel,
        "text": text
    }
    response = requests.post("https://slack.com/api/chat.postMessage", headers=headers, json=data)
    #print("💬 슬랙 응답:", response.json())
    print("💬 슬랙 응답:", text)

# DeepL 번역
def translate_text(text, source_lang, target_lang):
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "source_lang": source_lang,
        "target_lang": target_lang
    }
    response = requests.post(url, data=params)
    result = response.json()
    return result["translations"][0]["text"]

# 언어 감지 (DeepL이 자동 감지함)
def detect_lang(text):
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "target_lang": "EN"
    }
    res = requests.post(url, data=params)
    detected = res.json()["translations"][0]["detected_source_language"]
    print("🔍 감지된 언어:", detected)
    return detected

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json

    # Slack 인증 challenge
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    # 이벤트 처리
    if data.get("type") == "event_callback":
        event = data.get("event", {})
        if event.get("type") == "app_mention":
            user = event.get("user")
            text = event.get("text", "")
            channel = event.get("channel")

            # 멘션 부분 제거
            clean_text = ' '.join(text.split()[1:])

            source_lang = detect_lang(clean_text)
            if source_lang == "KO":
                target_lang = "JA"
            elif source_lang == "JA":
                target_lang = "KO"
            else:
                send_slack_message(channel, f"<@{user}> 죄송해요, 한국어/일본어만 지원돼요 🥲")
                return "OK"

            translated = translate_text(clean_text, source_lang, target_lang)
            send_slack_message(channel, f"<@{user}> 🌐 번역결과:\n> {translated}")

    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(debug=False, host="0.0.0.0", port=port)
