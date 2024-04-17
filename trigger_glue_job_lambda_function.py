import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    glue = boto3.client('glue')
    glue_job_name = "ecommerce_data_processing"

    response = glue.start_job_run(JobName=glue_job_name)
    job_run_id = response['JobRunId']

    print(f"Glue job started {glue_job_name} with run_id : {job_run_id}")

    return {
        'statusCode': 200,
        'body': f"Glue job {glue_job_name} started successfull"
    }