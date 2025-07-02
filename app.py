from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_story():
    data = request.get_json()
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    body = {
        "contents": [
            {
                "parts": [
                    {"text": f"Continue the story: {prompt}"}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, json=body)
        result = response.json()
        story = result['candidates'][0]['content']['parts'][0]['text']
        return jsonify({'story': story})
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Failed to generate story'}), 500

if __name__ == '__main__':
    app.run(debug=True)
