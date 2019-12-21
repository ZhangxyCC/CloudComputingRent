import json
import boto3

def lambda_handler(event, context):
    print(event['queryStringParameters']['q'])
    query = event['queryStringParameters']['q']
    print(query)
    client = boto3.client('lex-runtime')
    response = client.post_text(
            botName='ZillowTest',
            botAlias='projectfinal',
            userId="aaa",
            sessionAttributes={},
            requestAttributes={},
            inputText=query
        )
    print("response")
    return {
        'headers': {
            'Content-Type': 'application/json', 
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'},
        'statusCode': 200,
        'body': json.dumps(response['message'])
    }

    
