import json
import urllib.request
import urllib.parse
import certifi
import boto3
import time
import requests
import json
import copy
import random
import base64

def lambda_handler(event, context):
    # TODO implement
    # print(event)
    res = event.copy()
    #uid = res['uid']
    #res['uid']='lk2807@columbia.edu'
    #del(res['uid'])
    #test event:
    # {
    #     "uid": "test@test.com",
    #     "aptid": "000000001",
    #     "street": "113 St",
    # 	  "zipcode": "100013"
    # }   
    #
    # Information needed:
    # event:
    # {
    #   'uid': user id
    #   'aptid': 主键，下面的都可以为空
    #   'street': 
    # 	'zipcode':
    # 	'city':
    # 	'state':
    # 	'latitude': 目前不知道怎么搜 不会做地图的。。
    # 	'longitude': 
    # 	'bedrooms': 
    # 	'bathrooms': 
    # 	'appliances':
    # 	'homeDescription': 
    # 	'images': '[[图片网址]...]'
    #   'rentzestimate':
    #   'zestimate':
    # }
    res['aptid'] = ''.join(["%s" % random.randint(0, 9) for num in range(0, 12)])
    
    #upload image
    s3=boto3.resource('s3')
    object = s3.Object('zillow-photo',res['aptid']+'.jpg')
    # print(event['images'])
    object.put(ACL='public-read-write', Body=base64.b64decode(event['images']))
    res['images']=['https://zillow-photo.s3.amazonaws.com/'+res['aptid']+'.jpg']
    
    #latitude
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+res['street']+','+res['city']+','+res['state']+'&key=AIzaSyAQOZgHTjAuWNrbYCIErEYiE9bodk9PJ6g'
    response = json.loads(requests.get(url).text)
    #print("response",response)
    res['latitude'] = str(response['results'][0]['geometry']["location"]['lat'])
    res['longitude'] = str(response['results'][0]['geometry']["location"]['lng'])
    print('res',res)
    #User, Apartment DynamoDB table adds property
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1',endpoint_url='https://dynamodb.us-east-1.amazonaws.com', aws_secret_access_key='FksG44/KoG6ixlfHZ++IbOF4l6K95xevtE2odXOq', aws_access_key_id='AKIAS7DTXGU555MIXNNY')
    print('2')
    table = dynamodb.Table('Apartment')
    print('1')
    response = table.put_item(Item = res)
    table = dynamodb.Table('User')
    print('3')
    getproperty = table.get_item(Key={ 'uid': res['uid']  })
    if 'property' in getproperty['Item'].keys():
        getproperty['Item']['property'].append(res['aptid'])
    else:
        getproperty['Item']['property'] = [res['aptid']]
    print('4')
    response = table.delete_item(Key={ 'uid': res['uid']  })
    response = table.put_item(Item = getproperty['Item'])
    print(response)
    print("DynamoDB PutItem succeed")
    
    #Elastic search domain adds property
    region = "us-east-1"
    domain = "https://search-project-lqvsw62viekkaqfdvq7uw5rwla.us-east-1.es.amazonaws.com"
    index = "project"
    types = "houses"
    headers = { "Content-Type": "application/json" }
    url = domain + '/' + index +'/' + types+'/' + res["aptid"]	    
    r = requests.put(url,  data=json.dumps(res), headers=headers)
    print(r.text)
    print("ES PutItem succeed")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
