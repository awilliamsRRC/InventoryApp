import json
import os

import boto3
import uuid

from decimal import Decimal  # Import Decimal module

def lambda_handler(event, context):
    # Parse incoming JSON data
    try:
        data = json.loads(event['body'])
    except (KeyError, json.JSONDecodeError):
        return {
            'statusCode': 400,
            'body': json.dumps("Bad request. Please provide a valid JSON body.")
        }

    # Get the table name from environment variable
    table_name = os.getenv('TABLE_NAME', 'Inventory')

    # DynamoDB setup
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    # Generate a unique inventory item ID
    item_id = str(uuid.uuid4())

    # Validate required fields
    required_fields = ['item_name', 'item_description', 'item_qty', 'item_price', 'item_location_id']
    if not all(field in data for field in required_fields):
        return {
            'statusCode': 400,
            'body': json.dumps("Missing required fields in request.")
        }

    # Convert numeric fields to Decimal
    try:
        table.put_item(
            Item={
                'item_id': item_id,
                'item_name': data['item_name'],
                'item_description': data['item_description'],
                'item_qty': Decimal(str(data['item_qty'])),
                'item_price': Decimal(str(data['item_price'])),
                'item_location_id': int(data['item_location_id'])
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f"Inventory item '{data['item_name']}' added successfully with ID {item_id}.")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error adding inventory item: {str(e)}")
        }
