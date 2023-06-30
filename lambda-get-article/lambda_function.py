import os
import boto3

def lambda_handler(event, context):
    # Create a DynamoDB client
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
    
    # Specify the name of the DynamoDB table
    table_name = 'articles'
    
    # Retrieve the table
    table = dynamodb.Table(table_name)
    
    try:
        # Perform a scan operation to fetch all items from the table
        response = table.scan()
        
        # Extract the items from the response
        items = response['Items']
        
        # Return a proper response
        return {
            'statusCode': 200,
            'body': items
        }
    
    except Exception as e:
        # Handle any errors that occur
        return {
            'statusCode': 500,
            'body': str(e)
        }


# Locally Only
if __name__ == '__main__':

    event = {}

    context = None  # You can pass a mock context if needed
    response = lambda_handler(event, context)
    print(response)