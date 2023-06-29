from dotenv import load_dotenv
import os
import praw
from bardapi import Bard
import openai

load_dotenv()

reddit_clientid = os.getenv("REDDIT_CLIENTID")
reddit_clientsecret = os.getenv("REDDIT_CLIENTSECRET")
reddit_username = os.getenv("REDDIT_USERNAME")
reddit_password = os.getenv("REDDIT_PASSWORD")
reddit_useragent = os.getenv("REDDIT_USERAGENT")

bard_api_key = os.getenv("BARD_API_KEY")
openai_api_key = os.getenv("OPENAI_KEY")

print(reddit_password)
# bard = Bard(token=bard_api_key)
openai.api_key = os.getenv("OPENAI_KEY")

def get_top_reddit_post(subreddit):
    reddit = praw.Reddit(client_id=reddit_clientid,
                        client_secret=reddit_clientsecret,
                        user_agent=reddit_useragent)
    # print(reddit.read_only)
    subreddit = reddit.subreddit(subreddit)
    top_post = subreddit.top(limit=1, time_filter='month')

    return top_post

def summarize_post(post, subreddit):

    prompt = f"The top post on {subreddit} today was about {post.title}. Now, let's generate a very funny summary:"

    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        temperature=1,
        max_tokens=150
    )
    funny_summary = response.choices[0].text.strip()

    return funny_summary

def main():
    subreddit = "funny"
    top_post = get_top_reddit_post(subreddit)
    #print(top_post)
    for post in top_post:
        # print('Title:', post.title)
        # print('Content:', post.selftext)
        # print('---------------------')
         funny_summary = summarize_post(post, subreddit)

         print(f"Title: {post.title}")
         print(f"Funny Summary: {funny_summary}")

if __name__ == "__main__":
    main()
