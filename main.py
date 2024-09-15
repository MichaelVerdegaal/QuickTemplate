"""
-- Loading --

1. Input transaction file
2. Load it using a loader to a dataframe
3. Convert it to standardized columns:
- date
- account_name
- account_number
- amount
- description
- category (if available)
4. Load existing transaction file from source, if exists
        Step 4.1. If not exists, then save df to file
        Step 4.2. If it does exist, then append transactions, remove duplicates, save file

-- Classifying --
0. Edit categories.txt file if wanted
1. If not exist create repeat.txt
2. Load transactions.csv to df
3. Loop over every transaction in df
        3.1 If transaction has a class, skip it
        3.2 Else continue
                3.2.1 If transaction Name/Description in repeat.txt, give it that class
                3.2.2 If transaction has no class, classify it with suggestions from categories.txt. Ask if this is single-time only or repeat. If repeat put it  Name/Description in repeat.txt, and class all similar transactions. If single-time, only classify this transaction.
4. Save updated transactions to file again.


"""

import pandas as pd
from config import PROJECT_FOLDER, OUTPUT_FOLDER
from main.load import ing_loader

# from transformers import pipeline

# Load and preprocess data
df = ing_loader(
    PROJECT_FOLDER / "data" / "NL38INGB0001546874_01-01-2024_18-08-2024.csv"
)

# Set up zero-shot classifier
# zeroshot_classifier = pipeline(
#     "zero-shot-classification",
#     model="MoritzLaurer/deberta-v3-large-zeroshot-v2.0",
#     device=0,
# )

# Read budget categories from categories.txt
with open(PROJECT_FOLDER / "categories.txt", "r") as f:
    budget_categories = [line.strip() for line in f.readlines()]


"""
________________________________________________________________________
"""

transaction_df_path = OUTPUT_FOLDER / "transactions.csv"
# Check if the transaction file exists
if transaction_df_path.exists():
    # Load existing transactions
    existing_df = pd.read_csv(transaction_df_path)
    existing_df["date"] = pd.to_datetime(existing_df["date"])

    # Append new transactions
    combined_df = pd.concat([existing_df, df], ignore_index=True)

    # Remove duplicates based on all columns
    combined_df.drop_duplicates(
        inplace=True, subset=["date", "account_name", "account_number", "amount"]
    )

    # Save the updated DataFrame
    combined_df.to_csv(transaction_df_path, index=False)
    print(f"Updated transactions saved to {transaction_df_path}")
else:
    # If the file doesn't exist, save the current DataFrame
    df.to_csv(transaction_df_path, index=False)
    print(f"New transactions saved to {transaction_df_path}")
