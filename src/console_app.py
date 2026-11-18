import joblib
import pandas as pd

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.model import MODEL_FILE, BASELINE_FEATURES
from src.decisions import (
    validate_application_fields,
    validate_score,
    advisory_decision,
)
from datetime import datetime
from pathlib import Path


console = Console()


def get_float(prompt, minimum=None):
    """Request and validate a numeric value from the user."""

    while True:
        try:
            value = float(console.input(f"[cyan]>[/cyan] {prompt}: "))

            if minimum is not None and value < minimum:
                console.print(
                    f"[red]Value must be {minimum} or greater.[/red]"
                )
                continue

            return value

        except ValueError:
            console.print(
                "[red]Invalid input. Please enter a number.[/red]"
            )


def get_integer(prompt, minimum=None, maximum=None):
    """Request and validate a whole-number value."""

    while True:
        try:
            value = int(console.input(f"[cyan]>[/cyan] {prompt}: "))

            if minimum is not None and value < minimum:
                console.print(
                    f"[red]Value must be {minimum} or greater.[/red]"
                )
                continue

            if maximum is not None and value > maximum:
                console.print(
                    f"[red]Value must not exceed {maximum}.[/red]"
                )
                continue

            return value

        except ValueError:
            console.print(
                "[red]Invalid input. Please enter a whole number.[/red]"
            )


def collect_application():
    """Collect mortgage application information from the user."""

    console.print(
        Panel.fit(
            "[bold cyan]MORTGAGE REPAYMENT RISK ASSESSMENT[/bold cyan]\n"
            "Decision-support prototype",
            border_style="cyan",
        )
    )

    console.print(
        "\n[bold yellow]Mortgage and affordability[/bold yellow]"
    )

    annual_income = get_float(
        "Annual Income (£)",
        minimum=1
    )

    property_value = get_float(
        "Property Value (£)",
        minimum=1
    )

    deposit = get_float(
        "Deposit (£)",
        minimum=0
    )

    requested_loan = get_float(
        "Requested Loan (£)",
        minimum=1
    )

    monthly_debt = get_float(
        "Monthly Debt Commitments (£)",
        minimum=0
    )

    # region Automatically calculate 3 features.
    debt_to_income = (
        monthly_debt * 12
        ) / annual_income

    loan_to_value = (
        requested_loan / property_value
    ) * 100

    loan_to_income = (
        requested_loan / annual_income
    )
    # endregion

    console.print(
        "\n[bold yellow]Credit history[/bold yellow]"
    )

    credit_score = get_integer(
        "Credit Score",
        minimum=300,
        maximum=850
    )

    missed_payments = get_integer(
        "Missed Payments in Previous 24 Months",
        minimum=0,
        maximum=24
    )

    credit_utilisation = get_float(
        "Credit Utilisation (%)",
        minimum=0
    )

    while credit_utilisation > 100:
        console.print(
            "[red]Credit utilisation cannot exceed 100%.[/red]"
        )

        credit_utilisation = get_float(
            "Credit Utilisation (%)",
            minimum=0
        )

    previous_default = get_integer(
        "Previous Default (0 = No, 1 = Yes)",
        minimum=0,
        maximum=1
    )

    console.print(
        "\n[bold yellow]Employment and savings[/bold yellow]"
    )

    employment_years = get_float(
        "Employment Years",
        minimum=0
    )

    savings = get_float(
        "Savings (£)",
        minimum=0
    )

    console.print(
        "\n[bold yellow]Mortgage terms[/bold yellow]"
    )

    term_years = get_integer(
        "Mortgage Term (Years)",
        minimum=1
    )

    interest_rate = get_float(
        "Interest Rate (%)",
        minimum=0
    )

    return {
        "annual_income_gbp": annual_income,
        "property_value_gbp": property_value,
        "deposit_gbp": deposit,
        "requested_loan_gbp": requested_loan,

        "loan_to_value_pct": loan_to_value,
        "loan_to_income_ratio": loan_to_income,

        "monthly_debt_commitments_gbp": monthly_debt,
        "debt_to_income_ratio": debt_to_income,

        "credit_score": credit_score,
        "employment_years": employment_years,
        "savings_gbp": savings,

        "missed_payments_24m": missed_payments,
        "credit_utilisation_pct": credit_utilisation,
        "previous_default_flag": previous_default,

        "term_years": term_years,
        "interest_rate_pct": interest_rate,
    }


def score_application(application):
    """Generate the model's class-1 repayment-difficulty score."""

    validate_application_fields(
        application,
        BASELINE_FEATURES
    )

    if not MODEL_FILE.is_file():
        raise FileNotFoundError(
            "No trained model was found. "
            "Run python -m src.main first."
        )

    row = pd.DataFrame(
        [application],
        columns=BASELINE_FEATURES
    )

    model = joblib.load(MODEL_FILE)

    score = model.predict_proba(row)[0, 1]

    return validate_score(float(score))


def display_application(application):
    """Display the application values entered by the user."""

    table = Table(
        title="Applicant Information",
        show_header=True
    )

    table.add_column("Field", style="cyan")
    table.add_column("Value", justify="right")

    table.add_row(
        "Annual Income",
        f"£{application['annual_income_gbp']:,.2f}"
    )

    table.add_row(
        "Property Value",
        f"£{application['property_value_gbp']:,.2f}"
    )

    table.add_row(
        "Deposit",
        f"£{application['deposit_gbp']:,.2f}"
    )

    table.add_row(
        "Requested Loan",
        f"£{application['requested_loan_gbp']:,.2f}"
    )

    table.add_row(
        "Loan-to-Value",
        f"{application['loan_to_value_pct']:.2f}%"
    )

    table.add_row(
        "Loan-to-Income",
        f"{application['loan_to_income_ratio']:.2f}x"
    )

    table.add_row(
        "Monthly Debt Commitments",
        f"£{application['monthly_debt_commitments_gbp']:,.2f}"
    )

    table.add_row(
        "Debt-to-Income",
        f"{application['debt_to_income_ratio']:.1%}"
    )

    table.add_row(
        "Credit Score",
        str(application["credit_score"])
    )

    table.add_row(
        "Employment Years",
        f"{application['employment_years']:.1f}"
    )

    table.add_row(
        "Savings",
        f"£{application['savings_gbp']:,.2f}"
    )

    table.add_row(
        "Missed Payments (24m)",
        str(application["missed_payments_24m"])
    )

    table.add_row(
        "Credit Utilisation",
        f"{application['credit_utilisation_pct']:.2f}%"
    )

    table.add_row(
        "Previous Default",
        "Yes"
        if application["previous_default_flag"] == 1
        else "No"
    )

    table.add_row(
        "Mortgage Term",
        f"{application['term_years']} years"
    )

    table.add_row(
        "Interest Rate",
        f"{application['interest_rate_pct']:.2f}%"
    )

    console.print()
    console.print(table)


def display_decision(decision):
    """Display the advisory mortgage assessment."""

    risk_level = decision["risk_level"]

    if risk_level == "LOW RISK":
        colour = "green"

    elif risk_level == "MEDIUM RISK":
        colour = "yellow"

    else:
        colour = "red"

    console.print()

    console.print(
        Panel.fit(
            "[bold]MORTGAGE ASSESSMENT RESULT[/bold]",
            border_style=colour
        )
    )

    console.print(
        f"\nRepayment-Difficulty Score: "
        f"[bold {colour}]"
        f"{decision['risk_percentage']:.1f}%"
        f"[/bold {colour}]"
    )

    console.print(
        f"Risk Level: "
        f"[bold {colour}]"
        f"{risk_level}"
        f"[/bold {colour}]"
    )

    console.print(
        "\n[bold]Recommendation[/bold]"
    )

    console.print(
        decision["recommendation"]
    )

    console.print(
        "\n[bold]Advisory Reasoning[/bold]"
    )

    for reason in decision["reasoning"]:
        console.print(
            f"[cyan]>[/cyan] {reason}"
        )

    console.print()

    console.print(
        Panel(
            "[bold]ADVISORY ONLY[/bold]\n\n"
            "This prototype does not automatically approve or "
            "decline a mortgage.\n\n"
            "The machine-learning score represents estimated "
            "repayment-difficulty risk within the scope of the "
            "supplied synthetic dataset.\n\n"
            "Final mortgage assessment requires human review.",
            border_style="blue",
        )
    )
def export_assessment(application, decision):
    """Export to a text file."""

    export_folder = Path("exports")
    export_folder.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_path = export_folder / f"mortgage_assessment_{timestamp}.txt"

    with open(file_path, "w", encoding="utf-8") as file:

        file.write("MORTGAGE REPAYMENT RISK ASSESSMENT\n")
        file.write("=" * 50 + "\n\n")

        file.write("APPLICANT INFORMATION\n")
        file.write("-" * 50 + "\n")

        file.write(
            f"Annual Income: "
            f"£{application['annual_income_gbp']:,.2f}\n"
        )

        file.write(
            f"Property Value: "
            f"£{application['property_value_gbp']:,.2f}\n"
        )

        file.write(
            f"Deposit: "
            f"£{application['deposit_gbp']:,.2f}\n"
        )

        file.write(
            f"Requested Loan: "
            f"£{application['requested_loan_gbp']:,.2f}\n"
        )

        file.write(
            f"Loan-to-Value: "
            f"{application['loan_to_value_pct']:.2f}%\n"
        )

        file.write(
            f"Loan-to-Income: "
            f"{application['loan_to_income_ratio']:.2f}x\n"
        )

        file.write(
            f"Monthly Debt Commitments: "
            f"£{application['monthly_debt_commitments_gbp']:,.2f}\n"
        )

        file.write(
            f"Debt-to-Income Ratio: "
            f"{application['debt_to_income_ratio']:.1%}\n"
        )

        file.write(
            f"Credit Score: "
            f"{application['credit_score']}\n"
        )

        file.write(
            f"Employment Years: "
            f"{application['employment_years']:.1f}\n"
        )

        file.write(
            f"Savings: "
            f"£{application['savings_gbp']:,.2f}\n"
        )

        file.write(
            f"Missed Payments (24 months): "
            f"{application['missed_payments_24m']}\n"
        )

        file.write(
            f"Credit Utilisation: "
            f"{application['credit_utilisation_pct']:.2f}%\n"
        )

        previous_default = (
            "Yes"
            if application["previous_default_flag"] == 1
            else "No"
        )

        file.write(
            f"Previous Default: {previous_default}\n"
        )

        file.write(
            f"Mortgage Term: "
            f"{application['term_years']} years\n"
        )

        file.write(
            f"Interest Rate: "
            f"{application['interest_rate_pct']:.2f}%\n"
        )

        file.write("\nASSESSMENT RESULT\n")
        file.write("-" * 50 + "\n")

        file.write(
            f"Repayment-Difficulty Score: "
            f"{decision['risk_percentage']:.1f}%\n"
        )

        file.write(
            f"Risk Level: "
            f"{decision['risk_level']}\n"
        )

        file.write("\nRECOMMENDATION\n")
        file.write("-" * 50 + "\n")

        file.write(
            decision["recommendation"] + "\n"
        )

        file.write("\nADVISORY REASONING\n")
        file.write("-" * 50 + "\n")

        for reason in decision["reasoning"]:
            file.write(f"- {reason}\n")

        file.write("\nADVISORY NOTICE\n")
        file.write("-" * 50 + "\n")

        file.write(
            "This prototype provides decision support only. "
            "The assessment does not automatically approve or "
            "decline a mortgage. Final assessment requires "
            "human review.\n"
        )

    return file_path

def main():
    """Run the interactive mortgage decision-support system."""

    try:
        application = collect_application()

        display_application(application)

        score = score_application(application)

        decision = advisory_decision(
            score,
            application
        )

        display_decision(decision)

        console.print()

        export_choice = console.input("[yellow]Export Assessment? (Y/N)[/yellow]").strip().lower()

        if export_choice == "y":
            file_path = export_assessment(application, decision)
            console.print(
                f"\n[green]Assessment exported successfully:[/green]\n"
                f"{file_path}"
            )
        if export_choice =="n":
            console.print("[dim]Application now complete[/dim]")

    except ValueError as error:
        console.print(
            f"\n[bold red]APPLICATION VALIDATION ERROR[/bold red]\n"
            f"{error}"
        )

    except FileNotFoundError as error:
        console.print(
            f"\n[bold red]MODEL ERROR[/bold red]\n"
            f"{error}"
        )


if __name__ == "__main__":
    main()