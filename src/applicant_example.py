import joblib
import pandas as pd

from src.model import MODEL_FILE, BASELINE_FEATURES
from src.decisions import validate_application_fields, validate_score, advisory_decision, advisory_reasoning

EXAMPLE_APPLICATION = {
    'annual_income_gbp': 52000,
    'property_value_gbp': 240000,
    'deposit_gbp':15000,
    'requested_loan_gbp':225000,
    'loan_to_value_pct': 93.75,
    'loan_to_income_ratio': 4.61, 
    'monthly_debt_commitments_gbp': 157,
    'debt_to_income_ratio': 0.362, 
    'credit_score': 702,
    'employment_years': 5,
    'savings_gbp': 4500,
    'missed_payments_24m': 1, 
    'credit_utilisation_pct': 37.99,
    'previous_default_flag': 0, 
    'term_years': 20, 
    'interest_rate_pct': 4.8,
}


def score_example(application):
    """Generate model's estimated probability for class 1; no advice."""
    validate_application_fields(application, BASELINE_FEATURES)
    row = pd.DataFrame([application], columns=BASELINE_FEATURES)
    if not MODEL_FILE.is_file():
        raise FileNotFoundError(
            "No trained model: first run python -m src.main"
        )
    model = joblib.load(MODEL_FILE)
    score = model.predict_proba(row)[0, 1]
    return validate_score(float(score))


def main():
    score = score_example(EXAMPLE_APPLICATION)
    decision = advisory_decision(
        score,
        EXAMPLE_APPLICATION
    )

    print("MORTGAGE APPLICATION ASSESSMENT")
    print("Applicant details:")
    print(f"credit_score={EXAMPLE_APPLICATION['credit_score']}")
    print(f"debt_to_income_ratio={EXAMPLE_APPLICATION['debt_to_income_ratio']:.2f}")

    print(f"\nRepayment-difficulty probability: {decision['risk_percentage']:.1f}%")
    print(f"Risk Level: {decision['risk_level']}")
    print(f"\nRecommendation: {decision['recommendation']}")
    print("\nReasoning:")
    for reason in decision["reasoning"]:
        print(f"- {reason}")

    print("\nAdvisory Only:")
    print("The reasoning is only advisory, this does not automatically approve or decline a mortgage, human review is required.")


if __name__ == "__main__":
    main()
