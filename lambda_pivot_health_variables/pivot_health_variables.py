def pivot_variables(event, context):
    query_string_parameters = event['queryStringParameters']
    print(event)
    print(query_string_parameters)
    return {
        "statusCode": 200,
        "headers": {
          'Content-Type': 'application/json',
        },
        "body": {
          "message": f"this is the response. This is the event: {event}",
        },
    }
