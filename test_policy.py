from modules.policy_engine import evaluate_policy

ratios = {
    "debt_to_ebitda": 2.5,
    "profit_margin": 12
}

result = evaluate_policy(
    bank_name="SBI",
    credit_score=75,
    ratios=ratios,
    fraud_score=10
)

print(result)