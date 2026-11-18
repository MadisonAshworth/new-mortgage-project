from pathlib import Path
import pandas as pd
from rich.table import Table
from rich.console import Console

console = Console()

DATA_FILE = Path(__file__).resolve().parents[1] / 'data' / 'mortgage_data.csv'
TARGET = 'repayment_difficulty_12m'


def load_data(path=DATA_FILE):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f'Mortgage dataset not found: {path}')
    df = pd.read_csv(path)
    if df[TARGET].isna().any() or not set(df[TARGET].unique()).issubset({0, 1}):
        raise ValueError('Expected a complete binary repayment_difficulty_12m target')
    return df


def print_audit(df):
    # region Dataset Overview
    summary = Table(title="Dataset Overview")

    summary.add_column("Property")
    summary.add_column("Value")

    summary.add_row("Rows", str(df.shape[0]))
    summary.add_row("Columns", str(df.shape[1]))

    console.print(summary)
    # endregion

    console.print('\nData types:\n', df.dtypes.to_string())

    # region Missing Values
    missing = Table(title="Missing Values")

    missing.add_column("Column Header")
    missing.add_column("Missing Values")

    for col, count in df.isna().sum().items():
        missing.add_row(col, str(count))

    console.print(missing)
    #endregion

    console.print('\nTarget distribution:\n', df[TARGET].value_counts().sort_index().to_string())
    # region Target Distributions
    target = Table(title="Target Distribution")

    target.add_column("Class")
    target.add_column("Count")

    for value, count in df[TARGET].value_counts().sort_index().items():
        target.add_row(str(value), str(count))

    console.print(target)
    # endregion

    # region Numerical Summary
    numerical_df = df.describe().round(2)

    numerical = Table(title="Numerical Summary")

    numerical.add_column("Statistics", style="cyan")
    for col in numerical_df.columns:
        numerical.add_column(col, justify="right")

    for stat in numerical_df.index:
        row = [stat]
        for value in numerical_df.loc[stat]:
            row.append(str(value))
        numerical.add_row(*row)

    console.print(numerical)

    # endregion

if __name__ == '__main__':
    print_audit(load_data())
