import json
import os

import boto3

def lambda_handler(event, context):
    # DynamoDB resource
    dynamodb = boto3.resource("dynamodb")
    table_name = os.getenv("TABLE_NAME", "Inventory")
    table = dynamodb.Table(table_name)

    # Get item_id and location_id from path parameters
    if "pathParameters" not in event or "id" not in event["pathParameters"]:
        return {"statusCode": 400, "body": json.dumps("Missing 'id' path parameter.")}

    item_id = event["pathParameters"]["id"]
    location_id = event["pathParameters"].get("location_id")  # Add location_id to path parameters

    if not location_id:
        return {"statusCode": 400, "body": json.dumps("Missing 'location_id' path parameter.")}

    # Attempt to delete item
    try:
        response = table.delete_item(
            Key={
                "item_id": item_id,  # Partition key
                "location_id": location_id  # Sort key
            }
        )

        # Check if item was actually deleted
        if response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
            return {
                "statusCode": 200,
                "body": json.dumps(f"Item with ID {item_id} and Location ID {location_id} deleted successfully."),
            }
        else:
            return {
                "statusCode": 500,
                "body": json.dumps("Unexpected error during deletion."),
            }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps(f"Error deleting item: {str(e)}")}
