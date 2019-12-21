import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    # test event:
    # {
    #     "uid":"test@test.com",
    #     "property":[],
    #     "firstname":"te",
    #     "lastname":"st",
    #     "password":"12321"
    # }
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1',endpoint_url='https://dynamodb.us-east-1.amazonaws.com', aws_secret_access_key='FksG44/KoG6ixlfHZ++IbOF4l6K95xevtE2odXOq', aws_access_key_id='AKIAS7DTXGU555MIXNNY')
    table = dynamodb.Table('User')
    response = table.put_item(Item = event)
    print(response)
    print('Add user complete')
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
