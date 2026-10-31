
import json
import pandas as pd

with open("data/processed/events.json", encoding="utf-8") as f:
    events = json.load(f)

df = pd.DataFrame(events)

print("\nTotal events:", len(df))

print("\nEvent counts:")
print(df["event_type"].value_counts())

print("\nPayment status:")
print(df["payment_status"].value_counts())

print("\nTotal order revenue:")

revenue = df.loc[
    df["event_type"] == "order_placed",
    "total_amount"
].sum()

print(round(revenue, 2))

print("\nUnique customers:")
print(df["customer_id"].nunique())

print("\nUnique sessions:")
print(df["session_id"].nunique())
