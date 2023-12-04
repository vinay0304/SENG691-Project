import json
import tweepy

# Load Twitter API credentials
with open('../config/auth_tokens.json') as f:
    auth_tokens = json.load(f)

# Twitter API settings
consumer_key = auth_tokens['consumer_key']
consumer_secret = auth_tokens['consumer_secret']
access_token = auth_tokens['access_token']
access_token_secret = auth_tokens['access_token_secret']

# Setup Tweepy API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Scrape tweets related to "CompanyX"
company_tweets = tweepy.Cursor(api.search, q='CompanyX', lang='en').items()

# Print and process tweets (you can modify this part for your use case)
for tweet in company_tweets:
    tweet_text = tweet.text
    print(f'Scraped tweet: {tweet_text}')
    # Process the tweet (e.g., send it to Kafka for analysis)
