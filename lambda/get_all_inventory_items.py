import boto3
import json
import os

def lambda_handler(event, context):
    # Initialize a DynamoDB client
    dynamo_client = boto3.client('dynamodb')

    # Get the table name from environment variable
    table_name = os.getenv('TABLE_NAME', 'Inventory')  # Updated table name

    # Scan the table to retrieve all inventory items
    try:
        response = dynamo_client.scan(TableName=table_name)
        items = response['Items']

        # Convert DynamoDB data from dictionary format
        formatted_items = [{k: list(v.values())[0] for k, v in item.items()} for item in items]

        return {
            'statusCode': 200,
            'body': json.dumps(formatted_items, default=str)  # Format items properly
        }
    except Exception as e:
        print(f"Error fetching inventory: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }

