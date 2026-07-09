import joblib

# Load trained Isolation Forest model
model = joblib.load("fraud_model.pkl")


def predict_csv(df):

    # Remove Class column if present
    if "Class" in df.columns:
        df = df.drop("Class", axis=1)

    # Predict
    predictions = model.predict(df)

    # Create a copy of uploaded data
    result_df = df.copy()

    # Add Transaction ID
    result_df.insert(0, "Transaction ID", range(1, len(result_df) + 1))

    # Isolation Forest:
    #  1  -> Legitimate
    # -1  -> Fraud

    result_df["Prediction"] = predictions

    result_df["Prediction"] = result_df["Prediction"].replace({
        1: "Legitimate",
        -1: "Fraud"
    })

    total = len(result_df)
    fraud = len(result_df[result_df["Prediction"] == "Fraud"])
    legitimate = total - fraud

    # Keep only fraud transactions
    fraud_transactions = result_df[
        result_df["Prediction"] == "Fraud"
    ]

    return (
        total,
        fraud,
        legitimate,
        fraud_transactions
    )