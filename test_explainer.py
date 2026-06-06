from modules.explainer import explain_prediction

sample = {
    "debt_to_ebitda": 5.5,
    "profit_margin": 3,
    "debt_ratio": 0.7,
    "current_ratio": 1.0,
    "interest_coverage": 1.2,
    "revenue_growth": -10,
    "fraud_score": 60,
    "promoter_stake": 40
}

result = explain_prediction(sample)

print("\nTOP FACTORS")
print("=" * 50)

for factor in result["factors"]:
    print(factor)

print("\nChart generated successfully.")