import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# ============================================================
# STEP 1: Load and prepare dataset
# ============================================================

# Load dataset with semicolon separator
df = pd.read_csv("student-mat.csv", sep=";")

# Keep only the features you want
features = ["studytime", "failures", "absences", "G1", "G2", "G3"]
df = df[features]

# Create target column:
# Rule: if final grade G3 < 10 → High Risk (1), else Low Risk (0)
df["target"] = df["G3"].apply(lambda g: 1 if g < 10 else 0)

# ============================================================
# STEP 2: Train/test split
# ============================================================

X = df[features]
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ============================================================
# STEP 3: Train Random Forest model
# ============================================================

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ============================================================
# STEP 4: Save model and feature order
# ============================================================

joblib.dump(model, "risk_model.pkl")
joblib.dump(features, "risk_features.pkl")

print("✅ Model trained and saved successfully!")
