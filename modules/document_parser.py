import pdfplumber
import re
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_financial_metrics(text):
    metrics = {}

    # Revenue patterns
    revenue_patterns = [
        r"(?:total\s+)?revenue[:\s]+(?:rs\.?|₹|inr)?\s*([\d,\.]+)\s*(?:crore|cr|lakh|l)?",
        r"net\s+sales[:\s]+(?:rs\.?|₹)?\s*([\d,\.]+)",
        r"turnover[:\s]+(?:rs\.?|₹)?\s*([\d,\.]+)"
    ]
    for pattern in revenue_patterns:
        match = re.search(pattern, text.lower())
        if match:
            metrics["revenue"] = float(match.group(1).replace(",", ""))
            break

    # EBITDA
    ebitda_match = re.search(
        r"ebitda[:\s]+(?:rs\.?|₹)?\s*([\d,\.]+)", text.lower()
    )
    if ebitda_match:
        metrics["ebitda"] = float(ebitda_match.group(1).replace(",", ""))

    # Total Debt
    debt_match = re.search(
        r"(?:total\s+)?(?:debt|borrowings?)[:\s]+(?:rs\.?|₹)?\s*([\d,\.]+)",
        text.lower()
    )
    if debt_match:
        metrics["total_debt"] = float(debt_match.group(1).replace(",", ""))

    # Net Profit
    profit_match = re.search(
        r"(?:net\s+profit|pat)[:\s]+(?:rs\.?|₹)?\s*([\d,\.]+)",
        text.lower()
    )
    if profit_match:
        metrics["net_profit"] = float(profit_match.group(1).replace(",", ""))

    # Total Assets
    assets_match = re.search(
        r"total\s+assets[:\s]+(?:rs\.?|₹)?\s*([\d,\.]+)",
        text.lower()
    )
    if assets_match:
        metrics["total_assets"] = float(assets_match.group(1).replace(",", ""))

    return metrics

def calculate_ratios(metrics):
    ratios = {}
    try:
        if "total_debt" in metrics and "ebitda" in metrics and metrics["ebitda"] > 0:
            ratios["debt_to_ebitda"] = round(metrics["total_debt"] / metrics["ebitda"], 2)

        if "net_profit" in metrics and "revenue" in metrics and metrics["revenue"] > 0:
            ratios["profit_margin"] = round(
                (metrics["net_profit"] / metrics["revenue"]) * 100, 2
            )

        if "total_debt" in metrics and "total_assets" in metrics and metrics["total_assets"] > 0:
            ratios["debt_ratio"] = round(
                metrics["total_debt"] / metrics["total_assets"], 2
            )
    except Exception as e:
        print(f"Ratio calculation error: {e}")
    return ratios