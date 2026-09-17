# 🌙 NoorLearn + Real ML — VS Code Guide

This upgrades your project from "AI wrapper" to **AI app + real trained ML model**, built properly in VS Code, matching the rigor of your teacher's notebook.

---

## 1. One-Time VS Code Setup (today, ~30-40 min)

1. **Install Python** from python.org if you don't have it (check "Add to PATH" during install).
2. **Install VS Code extensions:** open VS Code → Extensions panel → install **"Python"** (by Microsoft) and **"Jupyter"** (by Microsoft). These let VS Code run notebooks and Python files directly.
3. **Create a project folder**, e.g. `NoorLearn/`. Put these files in it (I've prepared both — see below):
   - `Student_Risk_Prediction_ML.ipynb` (the training notebook)
   - `app.py` (the Flask backend)
4. **Install the Python packages** you need. Open VS Code's terminal (Terminal → New Terminal) and run:
   ```
   pip install pandas numpy matplotlib seaborn scikit-learn joblib flask flask-cors requests
   ```
5. **Download the dataset**: search "Student Performance Data Set UCI" or "student-mat.csv Kaggle" and download `student-mat.csv`. Place it in the same `NoorLearn/` folder.

---

## 2. Run the ML Notebook

1. Open `Student_Risk_Prediction_ML.ipynb` in VS Code.
2. Click "Select Kernel" (top right) → choose your Python installation.
3. Run cells top to bottom (Shift+Enter on each, or "Run All"). This mirrors your teacher's exact workflow: load data → clean → explore → encode → split → train 4 models → compare → pick Random Forest → save it.
4. At the end, you'll have 4 new files in your folder: `risk_model.pkl`, `risk_scaler.pkl`, `risk_encoders.pkl`, `risk_features.pkl`. These are your trained model, ready to be used by the app.

**What makes this notebook stand out (mention these in your pitch):**
- You defined the target label yourself (`Risk = G3 < 10`) instead of using a pre-made one — that's real problem-framing, not just running someone else's recipe.
- You deliberately dropped `G1`/`G2`/`G3` from the features (Step 10) — a classic ML mistake beginners make is leaving in a feature that leaks the answer. Explaining *why* you avoided this is a strong technical talking point.
- You compare 4 models and explicitly discuss why **recall** matters more than raw accuracy for an at-risk prediction (missing a struggling student is worse than a false alarm).

---

## 3. Run the Backend

1. Open `app.py`, find the line `GEMINI_API_KEY = "PASTE_YOUR_GEMINI_API_KEY_HERE"` and paste your real key from Google AI Studio.
2. In the VS Code terminal, run:
   ```
   python app.py
   ```
3. You should see it running on `http://127.0.0.1:5000`. Leave this terminal running while you use the app.

This one backend now does two jobs:
- `/predict-risk` — takes a student's data, returns a risk prediction from your trained model
- `/generate` — takes a system+user prompt, calls Gemini, returns the text (your API key never touches the browser)

---

## 4. Connect Your Frontend

Your existing `index.html` (from the earlier no-code plan) needs two small changes. Since you know basic code now, here's exactly what changes and why — copy this prompt to your AI chat along with your current `index.html`:

```
Here is my current index.html file:
[PASTE YOUR CURRENT FULL index.html CODE]

Please update it so that:
1. Instead of calling the Gemini API directly from JavaScript, every "Generate" button
   (Lesson Plan, Worksheet, Quiz, Question Paper, Feedback) now sends a POST request to
   http://127.0.0.1:5000/generate with JSON body { "system_prompt": "...", "user_prompt": "..." }
   using the same prompt text as before, and reads the "text" field from the JSON response.
2. In the "Analyze Students" section, add a new button "Predict Risk (ML)" next to each
   student row. When clicked, it sends a POST request to http://127.0.0.1:5000/predict-risk
   with that student's data as JSON, and displays the returned risk (0 or 1) and probability
   as a colored badge (red if at risk, green if not) next to their name.
3. Remove the old hardcoded Gemini API key from the JavaScript entirely, since it's no longer
   needed in the frontend.

Give me the complete updated index.html file.
```

Since your student marks table currently only has Name + Maths/Science/English marks, and the ML model expects the richer UCI-style fields (study time, absences, failures, etc.), the cleanest fix for a 1-week project is to **extend your student table** to also collect those extra fields when a teacher adds a student — ask your AI chat for that as a follow-up prompt once the above is working.

---

## 5. How This Fits Your Week

You don't need extra days — this replaces and upgrades what was already planned for **Day 4-5 (Analytics)**:
- Old plan: pure threshold logic (marks < 40 → flag)
- New plan: threshold logic **plus** a real trained ML risk score, displayed side-by-side, so you can honestly say "we use a trained Random Forest classifier, not just an if-statement"

Everything else in your 7-day plan (Lesson Plan, Worksheet, Quiz, Question Paper generators, Feedback, translation) stays exactly the same — they just now call your Flask backend instead of Gemini directly.

---

## 6. Pitch Line for This Upgrade

*"Most AI tools for teachers just wrap a chatbot. NoorLearn does that too — but our risk-prediction feature is a real trained machine learning model, evaluated across four algorithms, that learns from behavioral patterns like study time and absences to flag at-risk students before their grades reflect it."*

That sentence alone puts you in a different category than a team that only prompted an LLM.
