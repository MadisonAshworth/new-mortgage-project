import math
from numbers import Real

def validate_application_fields(application, required_fields):
    invalid = []

    for field in required_fields:
        value = application.get(field)

        if (
            value is None
            or (isinstance(value, str) and not value.strip())
            or (isinstance(value, Real) and not math.isfinite(value))
        ):
            invalid.append(field)

    if invalid:
        raise ValueError(
            f"Missing or invalid fields: {invalid}"
        )

    if "credit_score" in application:
        credit_score = application["credit_score"]

        if isinstance(credit_score, bool) or not isinstance(
            credit_score, Real
        ):
            raise ValueError(
                "Credit score must be numeric."
            )

        if not 300 <= credit_score <= 850:
            raise ValueError(
                "Credit score must be between 300 and 850."
            )

    if "debt_to_income_ratio" in application:
        debt_to_income = application["debt_to_income_ratio"]

        if debt_to_income < 0:
            raise ValueError(
                "Debt-to-income ratio cannot be negative."
            )

    if "loan_to_income_ratio" in application:
        loan_to_income = application["loan_to_income_ratio"]

        if loan_to_income < 0:
            raise ValueError(
                "Loan-to-income ratio cannot be negative."
            )

    if "credit_utilisation_pct" in application:
        credit_utilisation = application["credit_utilisation_pct"]

        if not 0 <= credit_utilisation <= 100:
            raise ValueError(
                "Credit utilisation must be between 0 and 100."
            )

    if "previous_default_flag" in application:
        previous_default = application["previous_default_flag"]

        if previous_default not in (0, 1):
            raise ValueError(
                "Previous default flag must be 0 or 1."
            )

    if "missed_payments_24m" in application:
        missed_payments = application["missed_payments_24m"]

        if (
            isinstance(missed_payments, bool)
            or not isinstance(missed_payments, Real)
            or missed_payments != int(missed_payments)
            or not 0 <= missed_payments <= 24
        ):
            raise ValueError(
                "Missed payments must be a whole number "
                "between 0 and 24."
            )

    return True

def validate_score(score):
    if isinstance(score, bool) or not isinstance(score, Real):
        raise ValueError('Model score must be numeric')
    if not math.isfinite(score) or not 0 <= score <= 1:
        raise ValueError('Model score must be finite and between 0 and 1')
    return float(score)


def advisory_decision(score, application):
    validate_score(score)
    risk_percentage = score * 100
    reasoning = advisory_reasoning(application)

    # region Risk Percentage
    if risk_percentage <= 30:
        risk_level = "LOW RISK"
        recommendation = "Recommended proceed with standard mortgage assessment."
    elif risk_percentage <= 60:
        risk_level = "MEDIUM RISK"
        recommendation = "Recommended manual review, refer for additional afforability checks."
    else:
        risk_level = "HIGH RISK"
        recommendation = "Recommended manual review required."
    return {
        "risk_percentage": risk_percentage,
        "risk_level": risk_level,
        "recommendation": recommendation,
        "reasoning": reasoning
    }
    # endregion

def advisory_reasoning(application):
    reasons = []

    credit_score = application["credit_score"]
    debt_to_income_ratio = application["debt_to_income_ratio"]
    loan_to_income_ratio = application["loan_to_income_ratio"]
    credit_utilisation_pct = application["credit_utilisation_pct"]
    previous_default_flag = application["previous_default_flag"]
    missing_payments = application["missed_payments_24m"]
    if credit_score < 600:
        reasons.append("Low credit score may indicate an increased credit risk")

    if debt_to_income_ratio > 0.50:
        reasons.append(f"Debt to Income Ratio {debt_to_income_ratio} is above 50%, indicating a potential high existing debt burden.")

    if loan_to_income_ratio > 5:
        reasons.append("Loan to Income Ratio is above 5.0, this indicates a potentially high loan amount request compared to annual income.")

    if previous_default_flag == 1:
        reasons.append("Applicant has a previous default recorded.")

    if credit_utilisation_pct > 50:
        reasons.append(f"Credit utilisation amount totally {credit_utilisation_pct} is over 50%, which is considerably high.")

    if missing_payments > 0:
        reasons.append(f"Applicant has a total of {int(missing_payments)}, recorded in the previous 24 months.")

    if not reasons:
        reasons.append("No advisory reasoning's were noted, ")

    return reasons
