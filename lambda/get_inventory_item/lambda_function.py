import boto3
import json
import os
from decimal import Decimal

# Helper to convert Decimal to float for JSON serialization
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def lambda_handler(event, context):
    # Setup DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table_name = os.getenv('TABLE_NAME', 'Inventory')
    table = dynamodb.Table(table_name)

    # Get item_id from path parameters
    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter.")
        }

    item_id = event['pathParameters']['id']

    # Query table by item_id
    try:
        response = table.get_item(
            Key={
                'item_id': item_id
            }
        )

        item = response.get('Item')
        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps("Item not found.")
            }

        return {
            'statusCode': 200,
            'body': json.dumps(item, cls=DecimalEncoder)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error retrieving item: {str(e)}")
        }
