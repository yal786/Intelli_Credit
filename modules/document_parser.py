import fitz
import re
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    try:
        text = ""

        doc = fitz.open(pdf_path)

        for page in doc:
            text += page.get_text()

        doc.close()

        return text

    except Exception as e:
        print(f"PDF Extraction Error: {e}")
        return ""


def extract_financial_metrics(text):
    metrics = {}

    text = text.lower()

    # Revenue patterns
    revenue_patterns = [
        r"(?:total\s+)?revenue[:\s]+(?:rs\.?|₹|inr)?\s*([\d,\.]+)",
        r"net\s+sales[:\s]+(?:rs\.?|₹|inr)?\s*([\d,\.]+)",
        r"turnover[:\s]+(?:rs\.?|₹|inr)?\s*([\d,\.]+)"
    ]

    for pattern in revenue_patterns:
        match = re.search(pattern, text)
        if match:
            metrics["revenue"] = float(match.group(1).replace(",", ""))
            break

    # EBITDA
    ebitda_match = re.search(
        r"ebitda[:\s]+(?:rs\.?|₹|inr)?\s*([\d,\.]+)",
        text
    )

    if ebitda_match:
        metrics["ebitda"] = float(
            ebitda_match.group(1).replace(",", "")
        )

    # Total Debt
    debt_match = re.search(
        r"(?:total\s+)?(?:debt|borrowings?)[:\s]+(?:rs\.?|₹|inr)?\s*([\d,\.]+)",
        text
    )

    if debt_match:
        metrics["total_debt"] = float(
            debt_match.group(1).replace(",", "")
        )

    # Net Profit / PAT
    profit_match = re.search(
        r"(?:net\s+profit|pat)[:\s]+(?:rs\.?|₹|inr)?\s*([\d,\.]+)",
        text
    )

    if profit_match:
        metrics["net_profit"] = float(
            profit_match.group(1).replace(",", "")
        )

    # Total Assets
    assets_match = re.search(
        r"total\s+assets[:\s]+(?:rs\.?|₹|inr)?\s*([\d,\.]+)",
        text
    )

    if assets_match:
        metrics["total_assets"] = float(
            assets_match.group(1).replace(",", "")
        )

    return metrics


def calculate_ratios(metrics):
    ratios = {}

    try:
        # Debt / EBITDA
        if (
            "total_debt" in metrics
            and "ebitda" in metrics
            and metrics["ebitda"] > 0
        ):
            ratios["debt_to_ebitda"] = round(
                metrics["total_debt"] / metrics["ebitda"],
                2
            )

        # Profit Margin
        if (
            "net_profit" in metrics
            and "revenue" in metrics
            and metrics["revenue"] > 0
        ):
            ratios["profit_margin"] = round(
                (metrics["net_profit"] / metrics["revenue"]) * 100,
                2
            )

        # Debt Ratio
        if (
            "total_debt" in metrics
            and "total_assets" in metrics
            and metrics["total_assets"] > 0
        ):
            ratios["debt_ratio"] = round(
                metrics["total_debt"] / metrics["total_assets"],
                2
            )

    except Exception as e:
        print(f"Ratio calculation error: {e}")

    return ratios