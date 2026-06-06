"""Entry point for the Intelli_Credit application."""

from modules.document_parser import DocumentParser
from modules.fraud_detector import FraudDetector
from modules.risk_model import RiskModel
from modules.explainer import Explainer
from modules.cam_generator import CAMGenerator
from modules.policy_engine import PolicyEngine


def main():
    print("Starting Intelli_Credit application...")

    parser = DocumentParser()
    fraud_detector = FraudDetector()
    risk_model = RiskModel()
    explainer = Explainer()
    cam_generator = CAMGenerator()
    policy_engine = PolicyEngine()

    print("Modules initialized:")
    print(f"- {parser.__class__.__name__}")
    print(f"- {fraud_detector.__class__.__name__}")
    print(f"- {risk_model.__class__.__name__}")
    print(f"- {explainer.__class__.__name__}")
    print(f"- {cam_generator.__class__.__name__}")
    print(f"- {policy_engine.__class__.__name__}")


if __name__ == "__main__":
    main()
