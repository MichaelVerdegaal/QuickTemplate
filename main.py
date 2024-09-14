import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datai
df = pd.read_csv("data/NL38INGB0001546874_01-01-2024_18-08-2024.csv",
                 sep=";")
df = df[["Date", "Name / Description", "Amount (EUR)", "Transaction type", "Notifications"]]

# Rename
df = df.rename(columns={"Date": "date",
                        "Name / Description": "description",
                        "Amount (EUR)": "amount",
                        "Transaction type": "category",
                        "Notifications": "extra"})

# Set date format
df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
# To numeric
df["amount"] = df["amount"].str.replace(",", ".")
df["amount"] = pd.to_numeric(df["amount"])

# Get unique transaction categories
categories = df["category"].unique().tolist()
print(categories)

# Split
plt.pie(df.groupby("category")["amount"].sum(), labels=categories, autopct='%.0f%%')
plt.show()

# Categorize
"""
Online Banking = Moving between my accounts | Manual payments to other accounts
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

Keep:
- Online banking
- SEPA direct debit
- Various
- Payment terminal
- iDEAL
- Cash machine
"""
...
