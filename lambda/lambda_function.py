# Final version: does the math AND stores the result in DynamoDB.

# import the JSON utility package
import json
# import the Python math library
import math

# import the AWS SDK (for Python the package name is boto3)
import boto3
# helpers for the current time
from time import gmtime, strftime

# create a DynamoDB object using the AWS SDK
dynamodb = boto3.resource('dynamodb')
# select our table. CHANGE THIS to the exact name of YOUR table
table = dynamodb.Table('PowerOfMathDatabase')


# define the handler function that the Lambda service uses as its entry point
def lambda_handler(event, context):

    # current time, calculated on EVERY call (see PROJECT_GUIDE.md, "Improvements")
    now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

    # extract the two numbers from the Lambda service's event object
    mathResult = math.pow(int(event['base']), int(event['exponent']))

    # write result and time to DynamoDB.
    # 'ID' must match the partition key of your table EXACTLY (case-sensitive!)
    table.put_item(
        Item={
            'ID': str(mathResult),
            'LatestGreetingTime': now
        })

    # return a properly formatted JSON object
    return {
        'statusCode': 200,
        'body': json.dumps('Your result is ' + str(mathResult))
    }
