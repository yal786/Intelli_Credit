import streamlit as st
import os
from modules.document_parser  import extract_text_from_pdf, extract_financial_metrics, calculate_ratios
from modules.fraud_detector    import detect_fraud_signals
from modules.risk_model        import predict_risk
from modules.explainer         import explain_prediction
from modules.cam_generator     import generate_cam
from modules.policy_engine     import evaluate_policy
import base64

st.set_page_config(page_title="Intelli-Credit", page_icon="🏦", layout="wide")
st.title("🏦 Intelli-Credit — AI Credit Appraisal Platform")

with st.sidebar:
    st.header("Company Details")
    company_name   = st.text_input("Company Name", "Acme Corp Ltd")
    sector         = st.text_input("Sector", "Manufacturing")
    loan_amount    = st.number_input("Loan Amount (₹ Crores)", 1.0, 500.0, 50.0)
    tenure         = st.number_input("Tenure (months)", 12, 120, 36)
    bank           = st.selectbox("Select Bank", ["SBI", "HDFC", "Kotak"])
    st.divider()
    st.header("Manual Financial Input")
    gst_revenue    = st.number_input("GST Revenue (₹ Cr)", 0.0, 1000.0, 100.0)
    bank_inflow    = st.number_input("Bank Inflow (₹ Cr)",  0.0, 1000.0, 85.0)
    current_ratio  = st.number_input("Current Ratio",       0.1, 5.0,    1.5)
    interest_cov   = st.number_input("Interest Coverage",   0.1, 10.0,   2.5)
    rev_growth     = st.number_input("Revenue Growth (%)",  -20.0, 50.0, 10.0)
    promoter_stake = st.number_input("Promoter Stake (%)",  0.0, 100.0,  55.0)

tab1, tab2, tab3, tab4 = st.tabs(["📄 Document Upload", "🔍 Analysis", "🏦 Bank Policy", "📑 CAM Report"])

with tab1:
    uploaded = st.file_uploader("Upload Financial Document (PDF)", type=["pdf"])
    if uploaded:
        with open("temp_doc.pdf", "wb") as f:
            f.write(uploaded.read())
        text    = extract_text_from_pdf("temp_doc.pdf")
        metrics = extract_financial_metrics(text)
        ratios  = calculate_ratios(metrics)
        st.session_state["metrics"] = metrics
        st.session_state["ratios"]  = ratios
        st.success("Document parsed successfully!")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Extracted Metrics")
            st.json(metrics)
        with col2:
            st.subheader("Calculated Ratios")
            st.json(ratios)

with tab2:
    if st.button("Run Full Analysis", type="primary"):
        metrics = st.session_state.get("metrics", {})
        ratios  = st.session_state.get("ratios",  {})

        fraud_result = detect_fraud_signals(gst_revenue, bank_inflow,
                                            metrics.get("revenue", gst_revenue))
        input_data = {
            "debt_to_ebitda":    ratios.get("debt_to_ebitda", 3.0),
            "profit_margin":     ratios.get("profit_margin",  8.0),
            "debt_ratio":        ratios.get("debt_ratio",     0.5),
            "current_ratio":     current_ratio,
            "interest_coverage": interest_cov,
            "revenue_growth":    rev_growth,
            "fraud_score":       fraud_result["fraud_score"],
            "promoter_stake":    promoter_stake,
        }
        risk_result   = predict_risk(input_data)
        explain_result= explain_prediction(input_data)

        st.session_state["fraud_result"]   = fraud_result
        st.session_state["risk_result"]    = risk_result
        st.session_state["explain_result"] = explain_result
        st.session_state["input_data"]     = input_data

        col1, col2, col3 = st.columns(3)
        col1.metric("Credit Score",  f"{risk_result['credit_score']}/100")
        col2.metric("Risk Level",    risk_result["risk_level"])
        col3.metric("Decision",      risk_result["approval"])

        st.subheader("Fraud Detection")
        if fraud_result["clean"]:
            st.success("No fraud signals detected")
        else:
            for flag in fraud_result["flags"]:
                if flag["type"] == "CRITICAL":
                    st.error(f"🚨 {flag['signal']} — {flag['detail']}")
                else:
                    st.warning(f"⚠️ {flag['signal']} — {flag['detail']}")

        st.subheader("Explainable AI — What drove this decision?")
        chart_data = explain_result["chart"]
        st.image(base64.b64decode(chart_data))

with tab3:
    if "risk_result" in st.session_state:
        ratios       = st.session_state.get("ratios", {})
        risk_result  = st.session_state["risk_result"]
        fraud_result = st.session_state["fraud_result"]

        policy_result = evaluate_policy(
            bank, risk_result["credit_score"],
            ratios, fraud_result["fraud_score"]
        )
        if policy_result["eligible"]:
            st.success(f"✅ Eligible for {bank} loan")
        else:
            st.error(f"❌ Does not meet {bank} policy requirements")

        for v in policy_result["violations"]:
            st.error(v)
        for p in policy_result["passed"]:
            st.success(p)

with tab4:
    if st.button("Generate CAM PDF") and "risk_result" in st.session_state:
        company_data = {"name": company_name, "sector": sector,
                        "loan_amount": loan_amount, "tenure": tenure}
        cam_file = generate_cam(
            company_data,
            st.session_state.get("metrics", {}),
            st.session_state.get("ratios",  {}),
            st.session_state["fraud_result"],
            st.session_state["risk_result"],
            st.session_state["explain_result"]["factors"]
        )
        with open(cam_file, "rb") as f:
            st.download_button("⬇️ Download CAM PDF", f, cam_file, "application/pdf")
        st.success("CAM generated!")