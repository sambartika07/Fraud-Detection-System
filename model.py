import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import accuracy_score
import joblib

# ---------------- LOAD DATASET ---------------- #

df = pd.read_csv("dataset/creditcard.csv")

# Faster training
df = df.sample(n=30000, random_state=42)

# ---------------- FEATURES ---------------- #

X = df.drop("Class", axis=1)

# ---------------- TRAIN MODEL ---------------- #

model = IsolationForest(
    contamination=0.002,
    random_state=42
)

model.fit(X)

# ---------------- TEST MODEL ---------------- #

predictions = model.predict(X)

# Isolation Forest:
# 1  = Normal
# -1 = Fraud

predictions = [1 if p == -1 else 0 for p in predictions]

accuracy = accuracy_score(df["Class"], predictions)

print(f"Model Accuracy: {accuracy:.4f}")

# ---------------- SAVE MODEL ---------------- #

joblib.dump(model, "fraud_model.pkl")

print("Isolation Forest model saved successfully!")