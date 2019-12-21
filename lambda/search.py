import json
import requests
import boto3
import time
import os
def search(intent):
    intent = intent['currentIntent']['slots']
    print(intent)
    
    #ELASTICSEARCH
    region = 'us-east-1'
    domain = 'https://search-project-lqvsw62viekkaqfdvq7uw5rwla.us-east-1.es.amazonaws.com/'
    index = 'project'
    headers = { "Content-Type": "application/json" }
    url = domain + index +'/'+'_search'   
    query = ''
    isstart = 0
    #bedroomnum, bathroomnum = 0,0
    for i in intent.keys():
        if i != 'property':
            if i == 'bathrooms':
                if isstart == 0:
                    query = i + ':"' +intent[i] + '.0" '
                    isstart = 1
                else:
                    query += 'AND ' +i + ':"' +intent[i] + '.0" '
            # elif i == 'latitude' or i == 'longitude':
            #     print(i)
            elif i == 'appliances':
                if intent[i]:
                    if isstart == 0:
                        query = i + ':"' +intent[i] + '" '
                        isstart = 1
                    else:
                        query += 'AND ' +i + ':"' +intent[i] + '" '
                    
            elif i == 'rentzestimate' or i == 'zestimate':
                print(i)
            else:
                if isstart == 0:
                    query = i + ':"' +intent[i] + '" '
                    isstart = 1
                else:
                    query += 'AND ' +i + ':"' +intent[i] + '" '
    print(query)
    r = requests.get(url,params={"q":query})
    print("below r.text")
    print(r.text)
    r1 = json.loads(r.text)
    res = []
    if r1['hits']['hits']:
        response = {
                    "dialogAction": {
                        "type": "Close",
                        "fulfillmentState": "Fulfilled",
                        "message": {
                            "contentType": "PlainText",
                            "content": "{\"Houses\":"+ str(r1['hits']['hits']).replace("\'", "\"") + "}"
                        }
                    }
                }
        return response
        
        
        
    else:
        response = {
                    "dialogAction": {
                        "type": "Close",
                        "fulfillmentState": "Fulfilled",
                        "message": {
                            "contentType": "PlainText",
                            "content": "No houses found."
                        }
                    }
                }
        return response
    
    
    
    
    
def lambda_handler(event, context):
    # TODO implement
    # direct search
    
    
    # example = {
    # "appliances": "Washer, Dishwasher, Dryer",
    # "bathrooms": "3.0",
    # "bedrooms": "2",
    # "city": "New York",
    # "latitude": "40.7238",
    # "longitude": "-73.988998",
    # "rentzestimate": 10899,
    # "state": "NY",
    # "street": "64 E 1st St APT 2",
    # "useCode": "Condominium",
    # "zestimate": 2236449,
    # "zipcode": "10003"
    # }
    
    
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    print(event)
    return search(event)
    
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
