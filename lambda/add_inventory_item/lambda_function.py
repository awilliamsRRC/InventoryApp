import json
import os

import boto3
import ulid  # Make sure the ULID module is available in your Lambda package


def lambda_handler(event, context):
    # Parse incoming request body
    try:
        data = json.loads(event["body"])
    except (KeyError, TypeError, json.JSONDecodeError):
        return {
            "statusCode": 400,
            "body": json.dumps("Bad request. Please provide a valid JSON body."),
        }

    # Get DynamoDB table name
    table_name = os.getenv("TABLE_NAME", "Inventory")

    # DynamoDB setup
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

    # Generate a ULID for item_id
    item_id = str(ulid.new())

    # Validate required fields
    required_fields = [
        "item_name",
        "item_description",
        "item_qty_on_hand",
        "item_price",
        "item_location_id",
    ]
    if not all(field in data for field in required_fields):
        return {
            "statusCode": 400,
            "body": json.dumps("Missing one or more required fields."),
        }

    # Insert item into table
    try:
        table.put_item(
            Item={
                "item_id": item_id,
                "item_name": data["item_name"],
                "item_description": data["item_description"],
                "item_qty_on_hand": int(data["item_qty_on_hand"]),
                "item_price": float(data["item_price"]),
                "item_location_id": int(data["item_location_id"]),
            }
        )
        return {
            "statusCode": 200,
            "body": json.dumps(f"Item {item_id} added successfully."),
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps(f"Error adding item: {str(e)}")}
