import boto3
import json

def lambda_handler(event, context):
    event_name = event["Records"][0]["eventName"]

    if event_name == "ObjectCreated:Put":
        # Initialize the Glue client
        glue_client = boto3.client('glue')
    
        # Name of the Glue crawler to start
        crawler_name = 'transactions-ecomm-data-crawler'
    
        try:
            # Start the Glue crawler
            response = glue_client.start_crawler(Name=crawler_name)
            print("Crawler started successfully:", response)
    
            #Return success response
            return {
                'statusCode': 200,
                'body': 'Glue crawler started successfully'
            }
        except Exception as e:
            print("Error starting Glue crawler:", e)
    
            #Return error response
            return {
                'statusCode': 500,
                'body': 'Error starting Glue crawler: ' + str(e)
            }