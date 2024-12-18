from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

TELEGRAM_BOT_TOKEN = '7765541043:AAHDPBTNvGZrRLFNs1w7l8rg1ECCQp21Apk'
TARGET_CHAT_ID = '-1002446713561'

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Check if file is present
        if 'document' not in request.files:
            return jsonify({"ok": False, "description": "No file provided"}), 400

        file = request.files['document']
        chat_id = request.form.get('chat_id')
        topic_id = request.form.get('topic_id')
        caption = request.form.get('caption', '')

        # Prepare files for upload
        files = {
            'document': (file.filename, file, file.content_type)
        }

        # Prepare data for Telegram API
        data = {
            'chat_id': chat_id,
            'message_thread_id': topic_id,
            'caption': caption,
            'parse_mode': 'Markdown'
        }

        # Send file to Telegram
        response = requests.post(
            f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument',
            data=data,
            files=files
        )

        # Return Telegram's response
        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({
            "ok": False,
            "description": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 50005))
    app.run(host='0.0.0.0', port=port)