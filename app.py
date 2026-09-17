"""
NoorLearn Backend — Flask
--------------------------
Runs two jobs:
1. Serves predictions from the trained Random Forest risk model
2. Proxies calls to the Gemini API

Run:
    python app.py

Requires:
    pip install flask flask-cors requests joblib pandas scikit-learn
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# ============================================================
# LOAD TRAINED ML MODEL
# ============================================================

model = joblib.load("risk_model.pkl")
encoders = joblib.load("risk_encoders.pkl")
feature_order = joblib.load("risk_features.pkl")


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

# IMPORTANT:
# Put your real Gemini API key between the quotes.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-3.1-flash-lite:generateContent"
)


# ============================================================
# GEMINI REQUEST WITH AUTOMATIC RETRY
# ============================================================

def generate_with_retry(url, headers, data, max_retries=5):

    for attempt in range(max_retries):

        try:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=60
            )

            print(
                f"Gemini attempt {attempt + 1}/{max_retries} "
                f"- status: {response.status_code}"
            )

            # Success
            if response.status_code == 200:
                return response

            # Temporary errors
            if response.status_code in (429, 500, 502, 503, 504):

                # 2, 4, 8, 16, 32 seconds
                wait_time = 2 ** attempt

                print(
                    f"Gemini temporarily unavailable "
                    f"({response.status_code}). "
                    f"Retrying in {wait_time} seconds..."
                )

                if attempt < max_retries - 1:
                    time.sleep(wait_time)
                    continue

            # Other errors should not be retried
            return response

        except requests.exceptions.Timeout:
            print("Gemini request timed out.")

            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                continue

            raise

        except requests.exceptions.RequestException as e:
            print("Gemini connection error:", e)

            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                continue

            raise

    return response


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "message": "NoorLearn backend is running"
    })


# ============================================================
# RISK PREDICTION
# ============================================================

@app.route("/predict-risk", methods=["POST"])
def predict_risk():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No JSON data received"
            }), 400

        row = pd.DataFrame([data])

        # Apply the SAME label encoders used during training
        for col, encoder in encoders.items():

            if col in row.columns:
                row[col] = encoder.transform(row[col])

        # Ensure column order matches training exactly
        row = row[feature_order]

        prediction = int(model.predict(row)[0])

        probability = float(
            model.predict_proba(row)[0][1]
        )

        return jsonify({
            "risk": prediction,
            "probability": round(probability, 3)
        })

    except Exception as e:

        print("PREDICT ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 400


# ============================================================
# GEMINI GENERATE
# ============================================================

# ============================================================
# GEMINI GENERATE
# ============================================================

@app.route("/generate", methods=["POST"])
def generate():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No JSON data received"
            }), 400

        system_prompt = data.get("system_prompt", "")
        user_prompt = data.get("user_prompt", "")

        if not user_prompt:
            return jsonify({
                "error": "user_prompt is required"
            }), 400

        payload = {
            "systemInstruction": {
                "parts": [
                    {"text": system_prompt}
                ]
            },
            "contents": [
                {
                    "parts": [
                        {"text": user_prompt}
                    ]
                }
            ]
        }

        response = requests.post(
            GEMINI_URL,
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": GEMINI_API_KEY
            },
            json=payload,
            timeout=60
        )

        print("Gemini status:", response.status_code)
        print("Gemini response:", response.text)

        if response.status_code != 200:
            return jsonify({
                "error": "Gemini API request failed",
                "details": response.text
            }), response.status_code

        result = response.json()

        candidates = result.get("candidates", [])

        if not candidates:
            return jsonify({
                "error": "Gemini returned no candidates",
                "details": result
            }), 502

        parts = candidates[0].get("content", {}).get("parts", [])

        if not parts:
            return jsonify({
                "error": "Gemini returned no text",
                "details": result
            }), 502

        text = parts[0].get("text", "")

        return jsonify({
            "text": text
        })

    except Exception as e:

        print("GENERATE ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )