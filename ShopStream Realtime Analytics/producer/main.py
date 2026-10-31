
import os
import json

from flask import Flask, jsonify, request
from google.cloud import pubsub_v1

from event_generator import generate_events

app = Flask(__name__)

PROJECT_ID = os.environ["PROJECT_ID"]
TOPIC_ID = os.environ["TOPIC_ID"]

publisher = pubsub_v1.PublisherClient()

topic_path = publisher.topic_path(
    PROJECT_ID,
    TOPIC_ID
)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "ShopStream Producer is running"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})


@app.route("/generate", methods=["POST"])
def generate():

    body = request.get_json(silent=True) or {}

    number_of_events = int(
        body.get("number_of_events", 10)
    )

    if not 1 <= number_of_events <= 500:
        return jsonify({
            "error": "Enter between 1 and 500 events"
        }), 400

    events = generate_events(number_of_events)

    published = 0

    for event in events:

        message = json.dumps(event).encode("utf-8")

        future = publisher.publish(
            topic_path,
            message,
            event_type=event["event_type"]
        )

        future.result(timeout=30)

        published += 1

    return jsonify({
        "message": "Events published successfully",
        "total_events": published
    })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )
