BANK_POLICIES = {
    "SBI": {
        "min_credit_score":    60,
        "max_debt_to_ebitda":  4.0,
        "min_profit_margin":   5.0,
        "max_debt_ratio":      0.65,
        "max_fraud_score":     30,
    },
    "HDFC": {
        "min_credit_score":    65,
        "max_debt_to_ebitda":  3.5,
        "min_profit_margin":   8.0,
        "max_debt_ratio":      0.55,
        "max_fraud_score":     25,
    },
    "Kotak": {
        "min_credit_score":    70,
        "max_debt_to_ebitda":  3.0,
        "min_profit_margin":   10.0,
        "max_debt_ratio":      0.50,
        "max_fraud_score":     20,
    },
}

def evaluate_policy(bank_name, credit_score, ratios, fraud_score):
    policy     = BANK_POLICIES.get(bank_name, BANK_POLICIES["SBI"])
    violations = []
    passed     = []

    checks = [
        ("credit_score",    credit_score,
         policy["min_credit_score"],   ">=", "Credit Score"),
        ("debt_to_ebitda",  ratios.get("debt_to_ebitda", 0),
         policy["max_debt_to_ebitda"], "<=", "Debt/EBITDA"),
        ("profit_margin",   ratios.get("profit_margin", 0),
         policy["min_profit_margin"],  ">=", "Profit Margin"),
        ("fraud_score",     fraud_score,
         policy["max_fraud_score"],    "<=", "Fraud Score"),
    ]
    for key, value, threshold, op, label in checks:
        ok = (value >= threshold if op == ">=" else value <= threshold)
        if ok:
            passed.append(f"✓ {label}: {value} (threshold: {op}{threshold})")
        else:
            violations.append(f"✗ {label}: {value} violates {op}{threshold}")

    return {
        "bank":       bank_name,
        "eligible":   len(violations) == 0,
        "violations": violations,
        "passed":     passed
    }