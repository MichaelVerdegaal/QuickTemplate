import json

from config import PROJECT_FOLDER, OUTPUT_FOLDER
from main.load import ing_loader
from transformers import pipeline

# Load and preprocess data
df = ing_loader(
    PROJECT_FOLDER / "data" / "NL38INGB0001546874_01-01-2024_18-08-2024.csv"
)

# Set up zero-shot classifier
zeroshot_classifier = pipeline(
    "zero-shot-classification",
    model="MoritzLaurer/deberta-v3-large-zeroshot-v2.0",
    device=0,
)

# Read budget categories from categories.txt
with open(PROJECT_FOLDER / "categories.txt", "r") as f:
    budget_categories = [line.strip() for line in f.readlines()]

# Set up json file to store transaction classifications
json_file_path = OUTPUT_FOLDER / "transaction_classifications.json"

# Initialize an empty dictionary to store classifications
transaction_classifications = {}

# Load existing classifications if the file exists
if json_file_path.exists():
    with json_file_path.open("r") as json_file:
        transaction_classifications = json.load(json_file)

# Iterate over each row
...
