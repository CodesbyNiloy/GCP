
import requests
import pandas as pd
import json
import os

API_URL = "https://randomuser.me/api/?results=100"

response = requests.get(API_URL, timeout=30)
response.raise_for_status()

data = response.json()

users = data["results"]

customers = []

for user in users:

    customer = {
        "customer_id": user["login"]["uuid"],
        "first_name": user["name"]["first"],
        "last_name": user["name"]["last"],
        "email": user["email"],
        "country": user["location"]["country"],
        "city": user["location"]["city"],
        "phone": user["phone"]
    }

    customers.append(customer)

os.makedirs("data/raw", exist_ok=True)

with open("data/raw/customers.json", "w", encoding="utf-8") as file:
    json.dump(customers, file, indent=4, ensure_ascii=False)

df = pd.DataFrame(customers)

df.to_csv("data/raw/customers.csv", index=False)

print("Total customers fetched:", len(customers))
print(df.head())

print("\nCustomer data saved successfully!")
