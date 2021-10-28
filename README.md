# Cloudfunction to BigQuery triggered by Pub/Sub
This function can be triggered either when called locally or as a Google Cloudfunction 
that is triggered by a pub-sub topic. 

The function currently creates some dummy data and saves it to an imaginery BigQuery dataset.
The dummy data can be replaced with an API call and the BigQuery table with the correct schema
must exist for the function to work.

It requires a table to already exist with the schema below.

## Logic Overview
The logic is simple and depends on the setup. It consists of 2 steps:

1. Get (create) data
2. Format and insert into BigQuery table

## BigQuery Schema
```json
"fields": [
  {
    "mode": "NULLABLE",
    "name": "bigquery_column_name_1",
    "type": "STRING"
  },
  {
    "mode": "NULLABLE",
    "name": "bigquery_column_name_2",
    "type": "STRING"
  },
  {
    "mode": "NULLABLE",
    "name": "uploaded_at",
    "type": "TIMESTAMP"
  }
]
  ```

## Environment variables
These are to be stored in a .env file when running locally or set in the Cloudfunction console when deployed.
Things such as API keys can be added to this.
```
BIGQUERY_DATASET={str: the name of the dataset}
BIGQUERY_TABLE={str: the name of the table}
ENVIRONMENT={str: 'local' if running locally else 'cloud'}
```

## Running locally
What you will need to do first:
1. Ensure a BigQuery table exists with the above schema
2. Create a .env file in the format above
3. Create a `bigquery_credentials.json` file with the service account credentials 
required to upload to BigQuery and read from Google Cloud storage. This will need to be stored in the `credentials` directory.
4. Create a `local_input.json` which would mimick data that would be sent in the Pub/Sub message.
For example:
 ```json
{
  "example": 1
}
```

Use the following command:
`sh local_run.sh`

## Running as a Cloudfunction
1. Ensure a BigQuery table exists with the above schema
2. Create a Cloudfunction with the above environment variables that is triggered by a Pub/Sub topic
3. Link it to a Google Cloud repository that mirrors this Github repository
4. Create a Cloud Scheduler job to target that pub-sub topic with a payload as in point 4 of 'Running locally'