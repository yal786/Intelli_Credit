import shap
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import io, base64

def explain_prediction(input_data: dict):
    model    = pickle.load(open("models/risk_model.pkl", "rb"))
    scaler   = pickle.load(open("models/scaler.pkl",     "rb"))
    features = ["debt_to_ebitda","profit_margin","debt_ratio",
                "current_ratio","interest_coverage","revenue_growth",
                "fraud_score","promoter_stake"]

    X = pd.DataFrame([input_data])[features]
    X_scaled = pd.DataFrame(scaler.transform(X), columns=features)

    explainer   = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_scaled)

    # Get top factors
    feature_impacts = []
    shap_vals = shap_values[1][0] if isinstance(shap_values, list) else shap_values[0]

    for feat, val, shap_val in zip(features, X.iloc[0], shap_vals):
        impact = "INCREASES RISK" if shap_val > 0 else "REDUCES RISK"
        feature_impacts.append({
            "feature": feat.replace("_", " ").title(),
            "value":   round(float(val), 2),
            "impact":  impact,
            "strength":abs(round(float(shap_val), 3))
        })

    # Sort by strength
    feature_impacts.sort(key=lambda x: x["strength"], reverse=True)

    # Generate chart
    fig, ax = plt.subplots(figsize=(8, 4))
    names   = [f["feature"] for f in feature_impacts[:6]]
    values  = [f["strength"] if f["impact"] == "INCREASES RISK"
               else -f["strength"] for f in feature_impacts[:6]]
    colors  = ["#D85A30" if v > 0 else "#1D9E75" for v in values]
    ax.barh(names, values, color=colors)
    ax.axvline(x=0, color="gray", linewidth=0.8)
    ax.set_xlabel("SHAP Impact on Risk")
    ax.set_title("Credit Decision Factors")
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=100)
    buf.seek(0)
    chart_b64 = base64.b64encode(buf.read()).decode()
    plt.close()

    return {"factors": feature_impacts[:6], "chart": chart_b64}