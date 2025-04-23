import json
import os
from decimal import Decimal

import boto3

# Helper to convert Decimal to float for JSON serialization
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

    # Get item_id and location_id from path parameters
    if "pathParameters" not in event or "id" not in event["pathParameters"] or "location_id" not in event["pathParameters"]:
        return {"statusCode": 400, "body": json.dumps("Missing 'id' or 'location_id' path parameter.")}

    item_id = event["pathParameters"]["id"]
    location_id = event["pathParameters"]["location_id"]  # Get location_id from path parameters

    # Query table by item_id and location_id
    try:
        response = table.get_item(Key={"item_id": item_id, "location_id": location_id})

        item = response.get("Item")
        if not item:
            return {"statusCode": 404, "body": json.dumps("Item not found.")}

        return {"statusCode": 200, "body": json.dumps(item, cls=DecimalEncoder)}

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error retrieving item: {str(e)}"),
        }
