
import json
import random
import uuid
import os

from datetime import datetime, timezone

# Load products
with open("data/raw/products.json", encoding="utf-8") as f:
    products = json.load(f)

# Load customers
with open("data/raw/customers.json", encoding="utf-8") as f:
    customers = json.load(f)


def create_event(event_type, customer, product, session_id,
                 quantity=1, order_id=None, payment_status=None):

    unit_price = float(product["price"])

    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "event_timestamp": datetime.now(timezone.utc).isoformat(),

        "session_id": session_id,
        "customer_id": customer["customer_id"],

        "product_id": product["id"],
        "product_name": product["title"],

        "category_id": product["category"]["id"],
        "category_name": product["category"]["name"],

        "quantity": quantity,
        "unit_price": unit_price,
        "total_amount": round(unit_price * quantity, 2),

        "order_id": order_id,
        "payment_status": payment_status,

        "country": customer["country"]
    }

    return event


def generate_events(number_of_sessions=100):

    events = []

    for _ in range(number_of_sessions):

        customer = random.choice(customers)
        product = random.choice(products)

        session_id = str(uuid.uuid4())

        # Event 1: Product click
        events.append(
            create_event(
                "product_click",
                customer,
                product,
                session_id
            )
        )

        # Event 2: Add to cart
        quantity = random.randint(1, 5)

        events.append(
            create_event(
                "add_to_cart",
                customer,
                product,
                session_id,
                quantity
            )
        )

        # Not every customer places an order
        if random.random() < 0.60:

            order_id = str(uuid.uuid4())

            # Event 3: Order placed
            events.append(
                create_event(
                    "order_placed",
                    customer,
                    product,
                    session_id,
                    quantity,
                    order_id
                )
            )

            # Event 4: Payment processed
            payment_status = random.choices(
                ["SUCCESS", "FAILED", "PENDING"],
                weights=[85, 10, 5],
                k=1
            )[0]

            events.append(
                create_event(
                    "payment_completed",
                    customer,
                    product,
                    session_id,
                    quantity,
                    order_id,
                    payment_status
                )
            )

    return events


if __name__ == "__main__":

    os.makedirs("data/processed", exist_ok=True)

    events = generate_events(100)

    output_file = "data/processed/events.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=4, ensure_ascii=False)

    print("Event generation completed!")

    print("Total events generated:", len(events))

    print("\nEvent distribution:")

    event_types = {}

    for event in events:
        event_type = event["event_type"]

        event_types[event_type] = (
            event_types.get(event_type, 0) + 1
        )

    for event_type, count in event_types.items():
        print(event_type, ":", count)

    print("\nSample event:")
    print(json.dumps(events[0], indent=4))

    print("\nEvents saved to:", output_file)
