from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.route("/generate", methods=["POST"])
def generate_story():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # Gemini API call (example using text-bison-001 or replace with correct one)
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    body = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(url, headers=headers, params=params, json=body)
    result = response.json()

    try:
        story = result["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"story": story})
    except Exception:
        return jsonify({"error": "Failed to generate story", "raw": result}), 500

# Optional: Health check route
@app.route("/")
def index():
    return "Story Generator backend is running."
