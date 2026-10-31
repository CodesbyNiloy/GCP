
import functions_framework
from google.cloud import bigquery

PROJECT_ID = "shopstream-realtime-analytics"
DATASET_ID = "shopstream_realtime"
TABLE_ID = "events_raw"

client = bigquery.Client(project=PROJECT_ID)


@functions_framework.cloud_event
def load_event_to_bigquery(cloud_event):

    data = cloud_event.data

    bucket_name = data["bucket"]
    file_name = data["name"]

    if not file_name.startswith("events/"):
        print(f"Skipping file: {file_name}")
        return

    source_uri = f"gs://{bucket_name}/{file_name}"

    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND
    )

    job = client.load_table_from_uri(
        source_uri,
        table_ref,
        job_config=job_config
    )

    job.result()

    print(f"Loaded {file_name} into {table_ref}")
