
import os
import json
import base64

from flask import Flask, request, jsonify
from google.cloud import storage
from google.api_core.exceptions import PreconditionFailed

app = Flask(__name__)

BUCKET_NAME = os.environ["BUCKET_NAME"]

storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)


@app.route("/", methods=["POST"])
def process_event():

    try:
        envelope = request.get_json()

        if not envelope or "message" not in envelope:
            return jsonify({"error": "Invalid Pub/Sub message"}), 400

        message = envelope["message"]

        decoded_data = base64.b64decode(
            message["data"]
        ).decode("utf-8")

        event = json.loads(decoded_data)

        message_id = message.get("messageId", "unknown")

        event_type = event.get("event_type", "unknown")

        # Create a unique file for each Pub/Sub message
        file_name = f"events/{message_id}.json"

        blob = bucket.blob(file_name)

        blob.upload_from_string(
            json.dumps(event),
            content_type="application/json",
            if_generation_match=0
        )

        return jsonify({
            "status": "success",
            "event_type": event_type,
            "file": file_name
        }), 200

    except PreconditionFailed:
        # Message was already stored during an earlier delivery
        return jsonify({"status": "already_processed"}), 200

    except Exception as e:
        print(f"Worker error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy",
        "service": "ShopStream Worker"
    })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )
