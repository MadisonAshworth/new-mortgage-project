# Mortgage Decision Support System

This project is a Python mortgage decision support prototype developed from Logistic Regression.

The system uses synthetic mortgage data to estimate the risk of `repayment_difficulty_12m`.

The output is advisory only and does not automatically approve or decline a mortgage.

## Run Instructions

Run the following commands from the project folder using Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m src.data
.\.venv\Scripts\python.exe -m src.main
.\.venv\Scripts\python.exe -m src.applicant_example
.\.venv\Scripts\python.exe -m src.console_app
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

If issues with additional packages, please install using the following;

```powershell
.\.venv\Scripts\python.exe -m pip install "pandas>=2.2,<3"
.\.venv\Scripts\python.exe -m pip install "scikit-learn>=1.5,<2"
.\.venv\Scripts\python.exe -m pip install "joblib>=1.4,<2"
.\.venv\Scripts\python.exe -m pip install rich
.\.venv\Scripts\python.exe -m pip install ipykernel
.\.venv\Scripts\python.exe -m pip install matplotlib
```

To see installed packages run:

```powershell
.\.venv\Scripts\python.exe -m pip list
```

## Dataset

The project uses the supplied synthetic mortgage dataset:

New Dataset:

```text
data/mortgage_data.csv
```

Original Dataset:

```text
data/A2_Mortgage_Credit_Risk_Dataset.csv
```

The cleaned dataset contains:

- 800 mortgage applications
- 18 fields
- No missing values
- `repayment_difficulty_12m` as the target variable
- A new column `loan_to_income_ratio` feature

## Model

The project uses Logistic Regression with:

- Median imputation
- Standard scaling
- Train/test split
- Majority-class reference model
- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC
- Confusion matrix

## Threshold Testing

Different classification thresholds were tested to investigate the balance between Precision and Recall.

| Threshold |  Accuracy | Precision |    Recall |  F1 Score |   ROC-AUC |
| --------: | --------: | --------: | --------: | --------: | --------: |
|       50% |     0.769 |     0.450 |     0.257 |     0.327 |     0.724 |
|       45% |     0.756 |     0.429 |     0.343 |     0.381 |     0.724 |
|       40% |     0.750 |     0.429 |     0.429 |     0.429 |     0.724 |
|   **35%** | **0.762** | **0.463** | **0.543** | **0.500** | **0.724** |
|       30% |     0.731 |     0.413 |     0.543 |     0.469 |     0.724 |

The **35% threshold** was selected because it provided the strongest balance in these experiments.

At 35%:

- Accuracy = 76.2%
- Precision = 46.3%
- Recall = 54.3%
- F1 Score = 0.500
- ROC-AUC = 0.724

F1 Calc: F1=2×Precision+Recall/Precision×Recall​
ROC-AUC cal = Receiver Operating Characteristic - Area Under the Curve (discriminatory capability)

Threshold selection and its limitations are discussed in the assignment evaluation.

## Advisory Risk Levels

The application converts the model score into an advisory risk category:

|            Score | Risk Level  |
| ---------------: | ----------- |
|        0% to 30% | Low Risk    |
| Above 30% to 60% | Medium Risk |
|        Above 60% | High Risk   |

The recommendation is for decision support only.

Final mortgage decisions require human review.

## Project Files

```text
src/data.py
```

Loads and audits the dataset.

```text
src/model.py
```

Trains and evaluates the Logistic Regression model.

```text
src/decisions.py
```

Contains validation, advisory rules and reasoning.

```text
src/applicant_example.py
```

Scores a sample mortgage applicant.

```text
src/console_app.py
```

Runs the interactive mortgage assessment system.

```text
mortgage_evaluation.ipynb
```

Contains model and testing evidence.

```text
tests/
```

Contains automated tests.

```text
exports/
```

Contains Console Apps Export when tested, any exports will be stored here.

## Data and Academic Integrity

The project uses synthetic data only.

The project was developed from module-provided starter code and extended independently for Assignment 2.

Module-provided code and permitted AI assistance should be acknowledged in accordance with the assignment brief.
