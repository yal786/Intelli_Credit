def detect_fraud_signals(gst_revenue, bank_inflow, reported_revenue):
    flags = []
    fraud_score = 0

    # Rule 1: Bank inflow should be at least 70% of GST revenue
    if gst_revenue > 0:
        bank_gst_ratio = bank_inflow / gst_revenue
        if bank_gst_ratio < 0.5:
            flags.append({
                "type": "CRITICAL",
                "signal": "Bank inflows are less than 50% of GST revenue",
                "detail": f"GST Revenue: ₹{gst_revenue}Cr | Bank Inflow: ₹{bank_inflow}Cr",
                "inference": "Possible circular trading or fake invoicing"
            })
            fraud_score += 40
        elif bank_gst_ratio < 0.7:
            flags.append({
                "type": "WARNING",
                "signal": "Bank inflows significantly lower than GST revenue",
                "detail": f"Ratio: {bank_gst_ratio:.2f} (expected > 0.7)",
                "inference": "Revenue may be partially inflated"
            })
            fraud_score += 20

    # Rule 2: Reported revenue vs GST revenue mismatch
    if reported_revenue > 0 and gst_revenue > 0:
        rev_mismatch = abs(reported_revenue - gst_revenue) / reported_revenue
        if rev_mismatch > 0.2:
            flags.append({
                "type": "WARNING",
                "signal": "Reported revenue and GST revenue differ by more than 20%",
                "detail": f"Reported: ₹{reported_revenue}Cr | GST: ₹{gst_revenue}Cr",
                "inference": "Possible under-reporting of GST or revenue inflation"
            })
            fraud_score += 25

    # Rule 3: Revenue growth check (if YoY data available)
    fraud_score = min(fraud_score, 100)

    return {
        "fraud_score": fraud_score,
        "risk_level": "HIGH" if fraud_score > 50 else "MEDIUM" if fraud_score > 25 else "LOW",
        "flags": flags,
        "clean": len(flags) == 0
    }


result = detect_fraud_signals(
    gst_revenue=100,
    bank_inflow=40,
    reported_revenue=120
)

print(result)