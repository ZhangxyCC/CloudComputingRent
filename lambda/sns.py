import json
import boto3

# test event
# {
#   "phonenum" : "6462490063",
#   "aptid" : "119912809"
# }


def getinfo(aptid):
    response = {} 
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1',endpoint_url='https://dynamodb.us-east-1.amazonaws.com', aws_secret_access_key='FksG44/KoG6ixlfHZ++IbOF4l6K95xevtE2odXOq', aws_access_key_id='AKIAS7DTXGU555MIXNNY')
    table = dynamodb.Table('Apartment')
    getuser = table.get_item(Key={'aptid': aptid})
    userid = getuser['Item']['uid']
    table = dynamodb.Table('User')
    getproperty = table.get_item(Key={ 'uid': userid  })
    if 'phone' not in getproperty['Item'].keys():
        response['phone'] = '6469635309(FreeRent Customer Service)'
    else:
        response['phone'] = getproperty['Item']['phone']
    
    #response['firstname'] = getproperty['Item']['firstname']
    response['name'] = getproperty['Item']['name']
    return response

def sendsns(response, phonenum):
    sns = boto3.client('sns')
    info = 'Thanks for using FreeRent, The right person to contact for this property is ' + response['name'] + \
        ' ' + ', whose phone number is ' + response['phone']
    sns.publish(
        Message = info,
        PhoneNumber = '+1' + phonenum
    )

def lambda_handler(event, context):
    # TODO implement
    print(event["aptid"])
    response = getinfo(event['aptid'])
    sendsns(response, event['phonenum'])
    print("sent to "+response['firstname'])
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
