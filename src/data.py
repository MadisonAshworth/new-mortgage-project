from pathlib import Path
import pandas as pd

DATA_FILE = Path(__file__).resolve().parents[1] / 'data' / 'mortgage_data.csv'
TARGET = 'repayment_difficulty_12m'


def load_data(path=DATA_FILE):
    """Load CSV and confirm the identifier and observed target exist."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f'Mortgage dataset not found: {path}')
    df = pd.read_csv(path)
    if df[TARGET].isna().any() or not set(df[TARGET].unique()).issubset({0, 1}):
        raise ValueError('Expected a complete binary repayment_difficulty_12m target')
    return df


def print_audit(df):
    """Show factual checks; learners must explain what the findings mean."""
    print('Rows and columns:', df.shape)
    print('\nData types:\n', df.dtypes.to_string())
    print('\nMissing values:\n', df.isna().sum().to_string())
    print('\nTarget distribution:\n', df[TARGET].value_counts().sort_index().to_string())
    print('\nNumerical Summary:\n', df.describe().to_string())

if __name__ == '__main__':
    print_audit(load_data())
