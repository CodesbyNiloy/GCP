
import requests
import pandas as pd
import json
import os

API_URL = "https://api.escuelajs.co/api/v1/categories"

response = requests.get(API_URL, timeout=30)
response.raise_for_status()

categories = response.json()

print("Total categories fetched:", len(categories))

os.makedirs("data/raw", exist_ok=True)

with open("data/raw/categories.json", "w", encoding="utf-8") as file:
    json.dump(categories, file, indent=4, ensure_ascii=False)

df = pd.json_normalize(categories)

df.to_csv("data/raw/categories.csv", index=False)

print("\nCategory preview:")
print(df.head())

print("\nCategory data saved successfully!")
