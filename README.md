# Intelli_Credit

A credit risk and fraud detection prototype with modular components for document parsing, risk scoring, explainability, and policy enforcement.

## Project Structure

- `data/` - raw data, datasets, or serialized artifacts
- `models/` - trained model files and model metadata
- `modules/` - application modules and core logic
  - `document_parser.py`
  - `fraud_detector.py`
  - `risk_model.py`
  - `explainer.py`
  - `cam_generator.py`
  - `policy_engine.py`
- `app.py` - application entry point
- `requirements.txt` - package dependencies

## Setup

1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the environment:
   ```bash
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run

```bash
python app.py
```
