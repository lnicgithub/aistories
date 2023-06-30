import os
import praw
import openai
import boto3
from datetime import date
import uuid

ssm = boto3.client('ssm', region_name='eu-west-2')

response = ssm.get_parameter(
           Name='REDDIT_CLIENTID',
           WithDecryption=True
         )
reddit_clientid = response['Parameter']['Value']

response = ssm.get_parameter(
           Name='REDDIT_CLIENTSECRET',
           WithDecryption=True
         )
reddit_clientsecret = response['Parameter']['Value']

response = ssm.get_parameter(
           Name='REDDIT_USERNAME',
           WithDecryption=True
         )
reddit_username = response['Parameter']['Value']

response = ssm.get_parameter(
           Name='REDDIT_PASSWORD',
           WithDecryption=True
         )
reddit_password = response['Parameter']['Value']

response = ssm.get_parameter(
           Name='REDDIT_USERAGENT',
           WithDecryption=True
         )
reddit_useragent = response['Parameter']['Value']

response = ssm.get_parameter(
           Name='OPENAI_KEY',
           WithDecryption=True
         )

openai.api_key = response['Parameter']['Value']

def get_top_reddit_post(subreddit, timefilter):
    reddit = praw.Reddit(client_id=reddit_clientid,
                        client_secret=reddit_clientsecret,
                        user_agent=reddit_useragent)
    
    subreddit = reddit.subreddit(subreddit)
    top_post = subreddit.top(limit=1, time_filter=timefilter)

    return top_post

def summarize_post(post, subreddit, timefilter):

    prompt = f"The top post on {subreddit} this {timefilter} was about {post.title}. Now, let's generate a very funny summary:"

    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        temperature=1,
        max_tokens=150
    )
    funny_summary = response.choices[0].text.strip()

    return funny_summary

def generate_record(title, summary):
    id = uuid.uuid4()

    today = date.today().isoformat()
    newItem = { 'Id': {}, 'Title': {}, 'summary': {}, 'timestamp': {} }

    newItem['Id']['S'] = str(id)
    newItem['Title']['S'] = title
    newItem['summary']['S'] = summary
    newItem['timestamp']['S'] = today

    return newItem

def lambda_handler(event, context):
    dynamodb = boto3.client('dynamodb', region_name='eu-west-2')
    subreddit = event['subreddit']
    timefilter = event['timefilter']
    top_post = get_top_reddit_post(subreddit, timefilter)

    for post in top_post:
         funny_summary = summarize_post(post, subreddit, timefilter)

         try:
            response = dynamodb.list_tables()            
         except Exception as e:
           return {
                'statusCode': 500,
                'body': e
            }

         else:
            try:
                newItem = generate_record(post.title, funny_summary)
            except Exception as e:                
                return {
                    'statusCode': 500,
                    'body': e
                }
            else:
                dynamodb.put_item(TableName='articles',Item=newItem)
                return {
                'statusCode': 200,
                'body': 'entry added'
            }

# Locally Only
if __name__ == '__main__':

    event = {
        'subreddit': 'news',
        'timefilter': 'month'
    }

    context = None  # You can pass a mock context if needed
    response = lambda_handler(event, context)
    print(response)