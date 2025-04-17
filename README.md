# Slack Real-time Translator Bot

This is a Flask-based Slack bot that translates messages in real-time using the DeepL API.

## Features

- Translates Slack messages in real-time
- Detects specific keywords and sends alert to KakaoTalk (WIP)
- Built with Flask and deployed using Railway

## Setup

Create a `.env` file with the following:

```
SLACK_BOT_TOKEN=your-token
SLACK_SIGNING_SECRET=your-secret
DEEPL_API_KEY=your-deepl-api-key
```

Run locally:

```bash
pip install -r requirements.local.txt
python app.py
```

## Deploy on Railway

- Railway uses `Procfile` to run: `gunicorn app:app`
- Add environment variables in the Railway dashboard

## Author

Jimmy Om (@jimmy-om)
