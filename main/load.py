"""
Contains loaders for different data sources (file only)

Output will result in unified dataframe:
- date
- account_name
- account_number
- amount
- description
- category (if available)
"""

import pandas as pd


def ing_loader(file_path):
    """Loader for ING bank transaction export

    Online Banking = Moving between accounts | Manual payments to other accounts
    Batch payment = Retour. Only 1 instance
    Cash machine = Cash withdrawal (ATM)
    Deposit = Cash deposit (ATM)
    Transfer = Rounding feature from savings | Retour
    SEPA direct debit = Automatic debit payments
    Various = ING account payments | Credit card repayment
    Payment terminal = Payments at card machine
    iDEAL = Payments via iDEAL
    ____________________________________________________________________
    Drop:
    - Batch payment
    - Deposit
    - Transfer

    Split:
    - Online banking --> Remove if extra contains 'From Oranje spaarrekening'
    """
    # Load and preprocess data
    df = pd.read_csv(file_path, sep=";")

    # Rename columns for consistency and clarity
    df = df.rename(
        columns={
            "Date": "date",
            "Name / Description": "account_name",
            "Account": "account_number",
            "Amount (EUR)": "amount",
            "Transaction type": "category",
            "Notifications": "description",
        }
    )

    # Select relevant columns
    df = df[
        ["date", "account_name", "account_number", "amount", "category", "description"]
    ]

    # Convert date and amount columns
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
    df["amount"] = pd.to_numeric(df["amount"].str.replace(",", "."))

    # Filter transactions
    df = df[~df["category"].isin(["Batch payment", "Deposit", "Transfer"])]
    mask = (df["category"] == "Online Banking") & (
        df["description"].str.contains("Oranje spaarrekening", case=False, na=False)
    )
    df = df[~mask]

    return df
