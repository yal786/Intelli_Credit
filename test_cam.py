from modules.cam_generator import generate_cam

company_data = {
    "name": "ABC Industries",
    "sector": "Manufacturing",
    "loan_amount": 50,
    "tenure": 60
}

metrics = {
    "revenue": 1000,
    "net_profit": 120,
    "total_assets": 1500
}

ratios = {
    "profit_margin": 12.0,
    "debt_to_ebitda": 2.5
}

fraud_result = {
    "fraud_score": 20,
    "risk_level": "LOW",
    "flags": []
}

risk_result = {
    "credit_score": 82,
    "risk_level": "LOW",
    "approval": "APPROVED",
    "risk_probability": 0.18
}

factors = [
    {
        "feature": "Fraud Score",
        "value": 20,
        "impact": "REDUCES RISK",
        "strength": 0.5
    },
    {
        "feature": "Profit Margin",
        "value": 12,
        "impact": "REDUCES RISK",
        "strength": 0.4
    }
]

pdf_file = generate_cam(
    company_data,
    metrics,
    ratios,
    fraud_result,
    risk_result,
    factors
)

print("Generated:", pdf_file)