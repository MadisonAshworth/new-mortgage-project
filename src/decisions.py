import math
from numbers import Real

def validate_application_fields(application, required_fields):
    invalid = []
    for field in required_fields:
        value = application.get(field)
        if (value is None or
            (isinstance(value, str) and not value.strip()) or
            (isinstance(value, Real) and not math.isfinite(value))):
            invalid.append(field)
    if invalid:
        raise ValueError(f'Missing or invalid fields: {invalid}')
    if "credit_utilisation_pct" in application:
        if not 0 <= application["credit_utilisation_pct"] <= 100:
            raise ValueError("Credit utilisatipon must be between 0 and 100")
    if "previous_default_flag" in application:
        if application["previous_default_flag"] not in (0, 1):
            raise ValueError("Previous default flag must be true(1) or false(0)")
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

    # region Risk Percentage
    if risk_percentage <= 30:
        risk_level = "LOW RISK"
        recommendation = "Recommended approval, proceed with stand mortage assessment."
    elif risk_percentage <= 60:
        risk_level = "MEDIUM RISK"
        recommendation = "Recommended manual review, refer for additional afforability checks."
    else:
        risk_level = "HIGH RISK"
        recommendation = "Recommended manual review required."
    return {
        "risk_percentage": risk_percentage,
        "risk_level": risk_level,
        "recommendation": recommendation
    }
    # endregion
