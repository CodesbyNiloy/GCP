
import requests
import pandas as pd
import json
import os

API_URL = "https://api.escuelajs.co/api/v1/products"

response = requests.get(API_URL, timeout=30)
response.raise_for_status()

products = response.json()

print("Total products fetched:", len(products))

os.makedirs("data/raw", exist_ok=True)

with open("data/raw/products.json", "w", encoding="utf-8") as file:
    json.dump(products, file, indent=4, ensure_ascii=False)

df = pd.json_normalize(products)

df.to_csv("data/raw/products.csv", index=False)

print("\nProduct preview:")
print(df.head())

print("\nProduct data saved successfully!")
