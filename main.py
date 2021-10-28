import os
import json
import base64
from google.cloud import bigquery
from google.oauth2 import service_account


def main(event, context):
    # if you require data from the Pub/Sub topic
    if os.environ['ENVIRONMENT'] == 'local':
        input = 'local_input.json'
        with open(input, 'r') as f:
            string_data = f.read()
    else:
        string_data = base64.b64decode(event['data']).decode('utf-8')
    data = json.loads(string_data)
    example = data['example']

    # example data - to be replaced by API call
    example_data = [
        {"column1": "blah", "column2": "another blah"},
        {"column1": "blah blah", "column2": "blar"}
    ]

    # configure BigQuery
    if os.environ['ENVIRONMENT'] == 'local':
        key_path = 'credentials/bigquery_credentials.json'
        credentials = service_account.Credentials.from_service_account_file(
            key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        bq_client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    else:
        bq_client = bigquery.Client()
    dataset = os.environ['BIGQUERY_DATASET']
    table = os.environ['BIGQUERY_TABLE']
    table_id = dataset + '.' + table

    # format output and save to BigQuery
    formatted_output = []
    for record in example_data:
        formatted = {
            'bigquery_column_name_1': record['column1'],
            'bigquery_column_name_2': record['column2'],
            'uploaded_at': 'AUTO'
        }
        formatted_output.append(formatted)

    # run/ show errors
    errors = bq_client.insert_rows_json(table_id, formatted_output)
    if errors == []:
        print('{} new rows have been added'.format(len(formatted_output)))
    else:
        print('Encountered errors while inserting rows: {}'.format(errors))