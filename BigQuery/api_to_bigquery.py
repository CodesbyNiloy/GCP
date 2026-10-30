
import requests
from google.cloud import bigquery

# Replace this with your actual GCP project ID
PROJECT_ID = "project-840baaf4-213b-416b-9ef"
DATASET_ID = "Ecommerce_Data"

client = bigquery.Client(project=PROJECT_ID)

# Fetch product data from the API
products_response = requests.get(
    "https://dummyjson.com/products?limit=0",
    timeout=30
)
products_response.raise_for_status()
products = products_response.json()["products"]

product_fields = [
    "id",
    "title",
    "category",
    "price",
    "discountPercentage",
    "rating",
    "stock",
    "brand"
]

products = [
    {field: product.get(field) for field in product_fields}
    for product in products
]

# Fetch shopping cart data from the API
carts_response = requests.get(
    "https://dummyjson.com/carts?limit=0",
    timeout=30
)
carts_response.raise_for_status()
carts = carts_response.json()["carts"]

# Flatten nested cart products into individual rows
cart_items = []

for cart in carts:
    for item in cart["products"]:
        cart_items.append({
            "cart_id": cart["id"],
            "user_id": cart["userId"],
            "product_id": item["id"],
            "product_title": item["title"],
            "price": item["price"],
            "quantity": item["quantity"],
            "total": item["total"],
            "discount_percentage": item["discountPercentage"],
            "discounted_total": item["discountedTotal"]
        })

# Define the products table schema
product_schema = [
    bigquery.SchemaField("id", "INT64"),
    bigquery.SchemaField("title", "STRING"),
    bigquery.SchemaField("category", "STRING"),
    bigquery.SchemaField("price", "FLOAT64"),
    bigquery.SchemaField("discountPercentage", "FLOAT64"),
    bigquery.SchemaField("rating", "FLOAT64"),
    bigquery.SchemaField("stock", "INT64"),
    bigquery.SchemaField("brand", "STRING"),
]

# Define the cart items table schema
cart_schema = [
    bigquery.SchemaField("cart_id", "INT64"),
    bigquery.SchemaField("user_id", "INT64"),
    bigquery.SchemaField("product_id", "INT64"),
    bigquery.SchemaField("product_title", "STRING"),
    bigquery.SchemaField("price", "FLOAT64"),
    bigquery.SchemaField("quantity", "INT64"),
    bigquery.SchemaField("total", "FLOAT64"),
    bigquery.SchemaField("discount_percentage", "FLOAT64"),
    bigquery.SchemaField("discounted_total", "FLOAT64"),
]

# Upload data into BigQuery
def load_data(rows, table_name, schema):
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition="WRITE_TRUNCATE"
    )

    job = client.load_table_from_json(
        rows, table_id, job_config=job_config
    )
    job.result()

    table = client.get_table(table_id)
    print(f"{table_name}: loaded {table.num_rows} rows")


load_data(products, "raw_products", product_schema)
load_data(cart_items, "raw_cart_items", cart_schema)

print("API ingestion completed successfully!")
