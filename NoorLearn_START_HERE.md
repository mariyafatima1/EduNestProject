# 🌙 NoorLearn — START HERE (Final Consolidated Roadmap)

This combines everything: the AI-generator app, the real ML model, and your classroom-differentiator features, into one sequence. Follow it in order — don't jump ahead.

**Files you already have from this conversation** (save them all in one project folder called `NoorLearn`):
- `Student_Risk_Prediction_ML.ipynb` — trains your ML model
- `app.py` — your Flask backend (serves ML predictions + proxies Gemini)
- (You'll build `index.html` fresh this week using the AI-chat prompts below)

---

## 🟢 DO THIS RIGHT NOW (before anything else, ~15 min)

1. Create one folder on your computer called `NoorLearn`. Put `Student_Risk_Prediction_ML.ipynb` and `app.py` inside it.
2. Install VS Code if you don't have it (code.visualstudio.com — free).
3. Open the `NoorLearn` folder in VS Code (File → Open Folder).
4. Install the **Python** and **Jupyter** extensions inside VS Code (Extensions icon on the left sidebar → search each → Install).
5. Go to **aistudio.google.com**, sign in, click "Get API key" → copy it somewhere safe. This is free, no card needed.

That's your entire setup. Everything from here is just working through the days.

---

## Day 1 — Get the ML model trained (do this first, it's independent of everything else)

1. Search and download `student-mat.csv` (UCI/Kaggle "Student Performance Data Set"). Put it in your `NoorLearn` folder.
2. Open `Student_Risk_Prediction_ML.ipynb` in VS Code.
3. Open the VS Code terminal (Terminal menu → New Terminal) and run:
   ```
   pip install pandas numpy matplotlib seaborn scikit-learn joblib flask flask-cors requests
   ```
4. Click "Select Kernel" top-right of the notebook → pick your Python.
5. Run every cell top to bottom (Shift+Enter, or "Run All").
6. Confirm 4 new files appeared in your folder: `risk_model.pkl`, `risk_scaler.pkl`, `risk_encoders.pkl`, `risk_features.pkl`.

**✅ Checkpoint:** You now have a real trained ML model sitting on disk. This is the hardest technical part of your whole project, and it's done on Day 1.

---

## Day 1 (continued) — Get the backend running

1. Open `app.py`, paste your real Gemini API key into the `GEMINI_API_KEY` line.
2. In the terminal, run:
   ```
   python app.py
   ```
3. You should see `Running on http://127.0.0.1:5000`. Leave this terminal open and running for the rest of the week whenever you're testing.

**✅ Checkpoint:** Your backend is alive, serving both the ML model and Gemini, safely, from one place.

---

## Day 2 — Build the Dashboard + Lesson Plan Generator (frontend)

Open a free AI chat (Claude.ai, ChatGPT, or Gemini). Paste this:

```
I'm building a web app called NoorLearn for teachers, using plain HTML, CSS, and JavaScript in
ONE single index.html file (no frameworks, no build tools). My backend is a Flask server already
running at http://127.0.0.1:5000 with two endpoints:

1. POST /generate — body: { "system_prompt": "...", "user_prompt": "..." }, returns { "text": "..." }
2. POST /predict-risk — body: student data fields, returns { "risk": 0 or 1, "probability": 0.0-1.0 }

Build me a complete index.html file with:
- A clean dashboard titled "NoorLearn" with subtitle "Your AI teaching assistant" and tagline
  "Connecting what you teach, test, and track — in one place."
- A "Good morning, Teacher!" greeting
- 4 buttons: "📝 Create Lesson Plan", "❓ Generate Quiz", "📄 Create Worksheet", "📊 Analyze Students"
- Clicking a button hides the dashboard and shows that section (placeholders for now except Lesson Plan)
- A working "Create Lesson Plan" section: form with Class, Subject, Topic, Duration (minutes),
  Student Level (dropdown). On submit, POST to http://127.0.0.1:5000/generate with:
  system_prompt: "You are an expert pedagogy consultant and curriculum designer for Indian school
  education (NCERT/CBSE aligned). You create structured, classroom-ready lesson plans for teachers.
  Always output in clean Markdown with the exact section headers provided."
  user_prompt: "Create a lesson plan for Class {class}, Subject {subject}, Topic {topic}, Duration
  {duration} minutes, Student level {level}. Output using exactly these sections: 1. Learning
  Objectives 2. Previous Knowledge Required 3. Introduction Activity 4. Explanation 5. Classroom
  Activity 6. Questions for Students 7. Assessment 8. Homework 9. Teaching Resources Needed"
- Show a loading spinner while waiting, display the result formatted nicely, add a "Save" button
  that stores it in localStorage, and a "Back to Dashboard" button
- Clean, modern styling (soft colors, rounded corners)

Give me the complete file, ready to copy-paste as-is.
```

Paste the resulting code into a new `index.html` file in your `NoorLearn` folder. Open it by right-clicking → "Open with Live Server" (install the free "Live Server" VS Code extension if you don't have it) — this runs your frontend properly instead of just double-clicking the file.

**✅ Checkpoint:** You can generate a real lesson plan through your own app.

---

## Day 3 — Worksheet + Quiz Generators

Same pattern as Day 2. For each, paste your **current full `index.html`** into the AI chat along with a request for that feature (I gave you the exact system/user prompts for Worksheet and Quiz in our earlier conversation — reuse them, just changing the API call to go through `http://127.0.0.1:5000/generate` instead of calling Gemini directly).

**✅ Checkpoint:** 3 generators working.

---

## Day 4 — Question Paper Generator + Student Table + Risk Prediction

1. Build the Question Paper Generator (same pattern, reuse that prompt).
2. Build the student marks table — but now include the extra fields your ML model needs (studytime, absences, failures, etc.), not just subject marks. Ask your AI chat:
   ```
   Here is my current index.html: [paste]

   In the "Analyze Students" section, build a form to add a student with these fields:
   name, school, sex, age, address, famsize, Pstatus, Medu, Fedu, Mjob, Fjob, reason, guardian,
   traveltime, studytime, failures, schoolsup, famsup, paid, activities, nursery, higher, internet,
   romantic, famrel, freetime, goout, Dalc, Walc, health, absences. Save each student to localStorage.
   Add a "Predict Risk" button per student that POSTs their data (excluding "name") to
   http://127.0.0.1:5000/predict-risk and shows a red badge "At Risk" or green badge "On Track"
   with the probability percentage next to their name.

   Give me the complete updated index.html file.
   ```

**✅ Checkpoint:** Your real ML model is now predicting risk inside your actual app.

---

## Day 5 — AI Analytics Narrative + Feedback + Translation + Your Differentiator Feature

1. Add the "Generate Insights" button (AI narrative summary) — reuse the Analytics prompt from earlier, routed through `/generate`.
2. Add Student Feedback generator + Hindi translation button (MyMemory API, no signup — reuse that exact prompt from earlier).
3. **Pick ONE differentiator feature to build today** (don't try both):
   - **WhatsApp send button (easiest, ~20 min):** After generating feedback, add a button that opens `https://wa.me/?text=YOUR_ENCODED_FEEDBACK_TEXT` — this opens WhatsApp with the message pre-filled, ready to send to a parent. No API, no signup, just a link. Ask your AI chat to add this exact button.
   - **OCR photo-to-marks (harder, ~1.5-2 hrs):** Ask your AI chat to add Tesseract.js (via CDN script tag) so a teacher can upload a photo of a handwritten mark sheet and the app extracts numbers into the table. More impressive, more time risk — only attempt if Day 1-4 went smoothly with time to spare.

**✅ Checkpoint:** All 7 features + your ML model + one classroom-specific differentiator, all working.

---

## Day 6 — Polish + Backup Plan

1. Add the "Time Saved" counter (reuse that prompt from earlier).
2. Click through every feature as a teacher would. Fix anything broken by describing the issue to your AI chat with your current code pasted in.
3. **Generate and screenshot 3-4 backup outputs** (one lesson plan, one quiz, one risk prediction, one translated feedback) — your safety net if WiFi/backend fails live.
4. Make sure `python app.py` is easy for you to restart quickly if it crashes mid-demo.

---

## Day 7 — Pitch Deck + Rehearsal

Build a 6-slide deck: Problem → What is NoorLearn → Live demo → What makes it different (real ML model + classroom-first design, not another LMS) → Roadmap → Thank you.

**Demo order:**
1. Dashboard (5 sec)
2. Lesson Plan — live generation
3. Quiz — interactive, polished
4. Analyze Students — show the ML risk prediction live, explain briefly that it's a trained Random Forest model, not a simple rule
5. Feedback → Translate to Hindi → (if built) send via WhatsApp — your closing wow moment
6. Close on your positioning line: *"We're not another LMS — we're built for the teacher an LMS was never built to serve."*

---

## If You Only Remember One Thing

**Start with Day 1's notebook, today.** It's self-contained, doesn't depend on anything else being built, and it's the part most likely to eat unexpected time (dataset download issues, package installs). Getting it done first removes your biggest risk and leaves the rest of the week for the parts you already have a clear, tested recipe for.
