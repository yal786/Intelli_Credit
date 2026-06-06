import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import shap
import pickle

def generate_training_data(n_samples=2000):
    """Generate realistic synthetic financial data for training"""
    np.random.seed(42)

    data = {
        "debt_to_ebitda":   np.random.uniform(0.5, 8.0, n_samples),
        "profit_margin":    np.random.uniform(-5, 30, n_samples),
        "debt_ratio":       np.random.uniform(0.1, 0.9, n_samples),
        "current_ratio":    np.random.uniform(0.5, 3.5, n_samples),
        "interest_coverage":np.random.uniform(0.5, 8.0, n_samples),
        "revenue_growth":   np.random.uniform(-20, 40, n_samples),
        "fraud_score":      np.random.uniform(0, 100, n_samples),
        "promoter_stake":   np.random.uniform(20, 75, n_samples),
    }
    df = pd.DataFrame(data)

    # Create risk labels based on financial logic
    risk_score = (
        (df["debt_to_ebitda"] > 4).astype(int) * 30 +
        (df["profit_margin"] < 5).astype(int) * 20 +
        (df["debt_ratio"] > 0.6).astype(int) * 25 +
        (df["current_ratio"] < 1.2).astype(int) * 15 +
        (df["fraud_score"] > 50).astype(int) * 35 +
        (df["interest_coverage"] < 1.5).astype(int) * 20 +
        np.random.normal(0, 5, n_samples)
    )
    df["high_risk"] = (risk_score > 50).astype(int)
    return df

def train_model():
    df = generate_training_data()
    features = ["debt_to_ebitda","profit_margin","debt_ratio",
                "current_ratio","interest_coverage","revenue_growth",
                "fraud_score","promoter_stake"]
    X = df[features]
    y = df["high_risk"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled  = scaler.transform(X_test)

    model = GradientBoostingClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    print(classification_report(y_test, model.predict(X_test_scaled)))

    # Save model and scaler
    pickle.dump(model,  open("models/risk_model.pkl", "wb"))
    pickle.dump(scaler, open("models/scaler.pkl",     "wb"))
    print("Model saved.")
    return model, scaler, features

def predict_risk(input_data: dict):
    model  = pickle.load(open("models/risk_model.pkl", "rb"))
    scaler = pickle.load(open("models/scaler.pkl",     "rb"))
    features = ["debt_to_ebitda","profit_margin","debt_ratio",
                "current_ratio","interest_coverage","revenue_growth",
                "fraud_score","promoter_stake"]

    X = pd.DataFrame([input_data])[features]
    X_scaled = scaler.transform(X)

    risk_proba = model.predict_proba(X_scaled)[0][1]
    credit_score = int((1 - risk_proba) * 100)

    return {
        "credit_score": credit_score,
        "risk_level": "LOW" if credit_score > 70
                      else "MEDIUM" if credit_score > 45
                      else "HIGH",
        "approval": "APPROVED" if credit_score > 60 else "REJECTED",
        "risk_probability": round(risk_proba, 3)
    }

if __name__ == "__main__":
    train_model()