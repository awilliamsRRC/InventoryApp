import json
import os

import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table_name = os.getenv("TABLE_NAME", "Inventory")
    table = dynamodb.Table(table_name)

    path_params = event.get("pathParameters", {})

    item_id = path_params.get("id")
    location_id = path_params.get("location_id")

    if not item_id or not location_id:
        return {
            "statusCode": 400,
            "body": json.dumps("Missing 'id' or 'location_id' path parameter.")
        }

    try:
        response = table.delete_item(
            Key={
                "item_id": item_id,
                "location_id": location_id
            }
        )

        if response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
            return {
                "statusCode": 200,
                "body": json.dumps(f"Item with ID {item_id} and Location ID {location_id} deleted successfully.")
            }
        else:
            return {
                "statusCode": 500,
                "body": json.dumps("Unexpected error during deletion.")
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error deleting item: {str(e)}")
        }
