import json
import os
from decimal import Decimal

import boto3

# Custom JSON encoder for Decimal
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def lambda_handler(event, context):
    # Setup DynamoDB
    dynamodb = boto3.resource("dynamodb")
    table_name = os.getenv("TABLE_NAME", "Inventory")
    table = dynamodb.Table(table_name)

    # Get location_id from path
    if "pathParameters" not in event or "id" not in event["pathParameters"]:
        return {
            "statusCode": 400,
            "body": json.dumps("Missing 'id' in path parameters."),
        }

    location_id = int(event["pathParameters"]["id"])  # Ensure it's an int

    # Query GSI that allows reverse lookup by location_id
    try:
        response = table.query(
            IndexName="LocationIndex",  # Ensure you're using the exact index name
            KeyConditionExpression=boto3.dynamodb.conditions.Key("location_id").eq(location_id)  # Querying based on location_id
        )

        items = response.get("Items", [])

        return {"statusCode": 200, "body": json.dumps(items, cls=DecimalEncoder)}

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error retrieving items by location: {str(e)}"),
        }
