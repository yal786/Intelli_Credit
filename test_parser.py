from modules.document_parser import *

pdf_path = "data/infosys_report.pdf"

text = extract_text_from_pdf(pdf_path)

print("TEXT EXTRACTED")
print("=" * 50)
print(text[:2000])

metrics = extract_financial_metrics(text)

print("\nMETRICS")
print("=" * 50)
print(metrics)

ratios = calculate_ratios(metrics)

print("\nRATIOS")
print("=" * 50)
print(ratios)