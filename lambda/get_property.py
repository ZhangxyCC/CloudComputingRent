import json
import boto3
# # test:
# {
#     "uid":"qz2374@columbia.edu"
# }

def lambda_handler(event, context):
    # TODO implement
    print(event)
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1',endpoint_url='https://dynamodb.us-east-1.amazonaws.com', aws_secret_access_key='FksG44/KoG6ixlfHZ++IbOF4l6K95xevtE2odXOq', aws_access_key_id='AKIAS7DTXGU555MIXNNY')
    table = dynamodb.Table('User')
    getinfo = table.get_item(Key={ 'uid': event['uid']})
    print(getinfo)
    
    property=getinfo['Item']['property']
    res = []
    if property:
        
        table = dynamodb.Table('Apartment')
        for p in property:
            getinfo = table.get_item(Key={ 'aptid': p  })['Item']
            res.append(getinfo)
    response={
        "uid":event['uid'],
        "property": res
    }
    return response
    # return {
    #     'statusCode': 200,
    #     'body': "{\"User\":"+ str(getinfo['Item']).replace("\'", "\"") + "}"
    # }
    
    
    
    
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Lambda!')
    # }
