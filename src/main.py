"""Run the supplied baseline only; assessed advisory rules are NOT provided."""
from src.data import load_data, print_audit
from src.model import BASELINE_FEATURES, MODEL_FILE, run_baseline
from rich.table import Table
from rich.console import Console
console = Console()


def report(name, result):
    # region Risk Table
    table = Table(title=name)

    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Accuracy", f"{result['accuracy']: .3f}")
    table.add_row("Precision", f"{result['precision_1']: .3f}")
    table.add_row("Recall", f"{result['recall_1']: .3f}")
    table.add_row("F1 Score", f"{result['f1_1']: .3f}")
    table.add_row("ROC AUC", f"{result['roc_auc']: .3f}")

    console.print(table)
    # endregion

    # region Confusion Matrix
    cm = result["confusion_matrix"]

    cm_table = Table(title="Confusion Matrix")

    cm_table.add_column("")
    cm_table.add_column("Predicted Negative")
    cm_table.add_column("Predicted Positive")

    cm_table.add_row("Actual Negative", str(cm[0][0]), str(cm[0][1]))
    cm_table.add_row("Actual Positive", str(cm[1][0]), str(cm[1][1]))

    console.print(cm_table)
    # endregion


def main():
    df = load_data()
    print_audit(df)
    reference_results, baseline_results = run_baseline(df)
    console.print('\n[yellow]Selected baseline features:[/yellow]')
    console.print(BASELINE_FEATURES)

    report('[green]Majority-class reference[/green]', reference_results)
    report('[cyan]Enhanced logistic-regression baseline[/cyan]', baseline_results)

    # region Model Comparion
    comparison = Table(title="Model Comparison")

    comparison.add_column("Metric")
    comparison.add_column("Majority Class")
    comparison.add_column("Enhanced Model")

    for metric in ("accuracy", "precision_1", "recall_1", "f1_1", "roc_auc"):
        comparison.add_row(
            metric,
            f"{reference_results[metric]:.3f}",
            f"{baseline_results[metric]:.3f}",
        )

    console.print(comparison)
    # endregion

    console.print(f'\n[purple]Trained baseline saved:[/purple] {MODEL_FILE}')
    console.print(
    "[bold yellow]Next Steps:[/bold yellow] "
    "justify/extend model, create decision rules, application integration, tests and improvement evidence."

)


if __name__ == '__main__':
    main()
