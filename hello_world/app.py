import json
import boto3

dynamodb = boto3.resource('dynamodb') #connect to dynamodb database
table = dynamodb.Table('Visitor') #get table from dynamodb database


def lambda_handler(event, context):
    #load parameters
    data = json.loads(event["body"])
    website = data['Site']
    
   
    try:
         # get item
        response = table.get_item(Key={'Site': website})
        item = response['Item']
    
        # update
        currentCount = item['count'] =  int(item['count']) + 1
    
        # put 
        table.put_item(Item=item)
    
    except:
        table.put_item(
            Item={
                'Site': website,
                'count': 1
            }
        )
        currentCount = 0
    #update count to return to site
    updatedCount = int(currentCount + 1)
    
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'count': updatedCount
        }),
        "isBase64Encoded": False
    }