import json
import os

import boto3


def lambda_handler(event, context):
    # DynamoDB resource (better than client for simplicity)
    dynamodb = boto3.resource("dynamodb")
    table_name = os.getenv("TABLE_NAME", "Inventory")
    table = dynamodb.Table(table_name)

    # Get item_id from path parameters
    if "pathParameters" not in event or "id" not in event["pathParameters"]:
        return {"statusCode": 400, "body": json.dumps("Missing 'id' path parameter.")}

    item_id = event["pathParameters"]["id"]

    # Attempt to delete item
    try:
        response = table.delete_item(Key={"item_id": item_id})

        # Check if item was actually deleted
        if response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
            return {
                "statusCode": 200,
                "body": json.dumps(f"Item with ID {item_id} deleted successfully."),
            }
        else:
            return {
                "statusCode": 500,
                "body": json.dumps("Unexpected error during deletion."),
            }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps(f"Error deleting item: {str(e)}")}
