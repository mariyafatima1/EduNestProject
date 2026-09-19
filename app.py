"""
EduNet Backend — Flask
--------------------------
Supports:
- Risk prediction with retrained Random Forest model
- Add student manually
- List students
- Upload CSV file
- Column mapping for flexible school data
- Gemini API proxy
- Resource management (save, list, get, delete)

Run:
    python app.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import requests
import os
import csv
import uuid
import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# ============================================================
# LOAD TRAINED ML MODEL
# ============================================================

model = joblib.load("risk_model.pkl")
feature_order = joblib.load("risk_features.pkl")

# ============================================================
# GEMINI CONFIGURATION
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-3.1-flash-lite:generateContent"
)

# ============================================================
# FILE LOCATIONS
# ============================================================

STUDENTS_FILE = "students.csv"
UPLOAD_FOLDER = "uploads"
RESOURCES_FILE = "resources.csv"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "EduNet backend is running"})

# ============================================================
# RISK PREDICTION
# ============================================================

@app.route("/predict-risk", methods=["POST"])
def predict_risk():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        row = pd.DataFrame([data])[feature_order]
        prediction = int(model.predict(row)[0])
        probability = float(model.predict_proba(row)[0][1])

        if probability >= 0.7:
            risk_level = "High Risk"
        elif probability >= 0.4:
            risk_level = "Medium Risk"
        else:
            risk_level = "Low Risk"

        return jsonify({
            "risk": prediction,
            "probability": round(probability, 3),
            "riskLevel": risk_level
        })

    except Exception as e:
        print("PREDICT ERROR:", e)
        return jsonify({"error": str(e)}), 400

# ============================================================
# ADD STUDENT MANUALLY
# ============================================================

@app.route("/add-student", methods=["POST"])
def add_student():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        file_exists = os.path.isfile(STUDENTS_FILE)
        with open(STUDENTS_FILE, mode="a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["name","studytime","failures","absences","G1","G2","G3"])
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)

        return jsonify({"message": "Student added successfully", "student": data})

    except Exception as e:
        print("ADD STUDENT ERROR:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/list-students", methods=["GET"])
def list_students():
    try:
        if not os.path.isfile(STUDENTS_FILE):
            return jsonify([])

        with open(STUDENTS_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            students = list(reader)

        return jsonify(students)

    except Exception as e:
        print("LIST STUDENTS ERROR:", e)
        return jsonify({"error": str(e)}), 500

# ============================================================
# UPLOAD STUDENTS FILE
# ============================================================

@app.route("/upload-students", methods=["POST"])
def upload_students():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        df = pd.read_csv(filepath, sep=";")  # adjust if comma separated
        headers = list(df.columns)

        return jsonify({"filepath": filepath, "headers": headers})

    except Exception as e:
        print("UPLOAD ERROR:", e)
        return jsonify({"error": str(e)}), 500

# ============================================================
# MAP COLUMNS TO REQUIRED FEATURES
# ============================================================

@app.route("/map-columns", methods=["POST"])
def map_columns():
    try:
        data = request.get_json()
        filepath = data["filepath"]
        mapping = data["mapping"]

        df = pd.read_csv(filepath, sep=";")
        df = df.rename(columns=mapping)

        required = ["studytime","failures","absences","G1","G2","G3"]
        for col in required:
            if col not in df.columns:
                return jsonify({"error": f"Missing column after mapping: {col}"}), 400

        results = []
        for _, row in df.iterrows():
            student = row[feature_order].to_frame().T
            prediction = int(model.predict(student)[0])
            probability = float(model.predict_proba(student)[0][1])

            if probability >= 0.7:
                risk_level = "High Risk"
            elif probability >= 0.4:
                risk_level = "Medium Risk"
            else:
                risk_level = "Low Risk"

            results.append({
                "name": row.get("name", "Unknown"),
                "risk": prediction,
                "probability": round(probability, 3),
                "riskLevel": risk_level
            })

        return jsonify(results)

    except Exception as e:
        print("MAP ERROR:", e)
        return jsonify({"error": str(e)}), 500

# ============================================================
# RESOURCE MANAGEMENT
# ============================================================

@app.route("/save-resource", methods=["POST"])
def save_resource():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        resource_id = str(uuid.uuid4())
        title = data.get("title", "Untitled")
        content = data.get("content", "")
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        file_exists = os.path.isfile(RESOURCES_FILE)
        with open(RESOURCES_FILE, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id","title","content","created_at"])
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                "id": resource_id,
                "title": title,
                "content": content,
                "created_at": created_at
            })

        return jsonify({"message": "Resource saved", "id": resource_id})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/list-resources", methods=["GET"])
def list_resources():
    try:
        if not os.path.isfile(RESOURCES_FILE):
            return jsonify([])

        with open(RESOURCES_FILE, "r") as f:
            reader = csv.DictReader(f)
            resources = list(reader)

        return jsonify(resources)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get-resource/<resource_id>", methods=["GET"])
def get_resource(resource_id):
    try:
        if not os.path.isfile(RESOURCES_FILE):
            return jsonify({"error": "No resources found"}), 404

        with open(RESOURCES_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["id"] == resource_id:
                    return jsonify(row)

        return jsonify({"error": "Resource not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/delete-resource/<resource_id>", methods=["DELETE"])
def delete_resource(resource_id):
    try:
        if not os.path.isfile(RESOURCES_FILE):
            return jsonify({"error": "No resources found"}), 404

        rows = []
        deleted = False
        with open(RESOURCES_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["id"] != resource_id:
                    rows.append(row)
                else:
                    deleted = True

        if not deleted:
            return jsonify({"error": "Resource not found"}), 404

        with open(RESOURCES_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id","title","content","created_at"])
            writer.writeheader()
            writer.writerows(rows)

        return jsonify({"message": "Resource deleted"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# GEMINI GENERATE
# ============================================================

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        system_prompt = data.get("system_prompt", "")
        user_prompt = data.get("user_prompt", "")

        if not user_prompt:
            return jsonify({"error": "user_prompt is required"}), 400

        payload = {
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"parts": [{"text": user_prompt}]}]
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

        if response.status_code != 200:
            return jsonify({"error": "Gemini API request failed", "details": response.text}), response.status_code

        result = response.json()
        candidates = result.get("candidates", [])
        if not candidates:
            return jsonify({"error": "Gemini returned no candidates", "details": result}), 502

        parts = candidates[0].get("content", {}).get("parts", [])
        if not parts:
            return jsonify({"error": "Gemini returned no text", "details": result}), 502

        text = parts[0].get("text", "")
        return jsonify({"text": text})

    except Exception as e:
        print("GENERATE ERROR:", e)
        return jsonify({"error": str(e)}), 500

# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":
    app.run(debug=True, port=5000)