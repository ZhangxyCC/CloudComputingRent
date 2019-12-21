import json
import urllib.request
import urllib.parse
import certifi
import boto3
import time
import requests
import json
import copy
def lambda_handler(event, context):
    # TODO implement
    print(event)
    #test event:
    # {
    #     "uid":"lk2807@columbia.edu",
    #     "aptid":"000000001"
    # }   
    
    # Information needed:
    # event:
    # {
    #   'uid':
    #   'aptid':
    # }
    # User DynamoDB table delete property
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1',endpoint_url='https://dynamodb.us-east-1.amazonaws.com', aws_secret_access_key='FksG44/KoG6ixlfHZ++IbOF4l6K95xevtE2odXOq', aws_access_key_id='AKIAS7DTXGU555MIXNNY')
    table = dynamodb.Table('Apartment')
    response = table.delete_item(Key={ 'aptid': event['aptid']})
    table = dynamodb.Table('User')
    getproperty = table.get_item(Key={ 'uid': event['uid']  })
    getproperty['Item']['property'].remove(event['aptid'])
    response = table.delete_item(Key={ 'uid': event['uid']  })
    response = table.put_item(Item = getproperty['Item'])
    print(response)
    print("DynamoDB PutItem succeed")
    
    #Elestic search delete property:
    region = "us-east-1"
    domain = "https://search-project-lqvsw62viekkaqfdvq7uw5rwla.us-east-1.es.amazonaws.com"
    index = "project"
    types = "houses"
    headers = { "Content-Type": "application/json" }
    url = domain + '/' + index +'/' + types+'/' + event["aptid"]      
    #r = requests.put(url,  data=json.dumps(res), headers=headers)
    r = requests.delete(url)
    print("ES DeleteItem succeed")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
