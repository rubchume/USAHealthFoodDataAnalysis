import json


def pivot_variables(event, context):
    print(event)
    return {"statusCode": 200, "body": json.dumps(event["queryStringParameters"])}
