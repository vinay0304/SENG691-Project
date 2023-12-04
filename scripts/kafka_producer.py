import json
from kafka import KafkaProducer
from tweepy import OAuthHandler, Stream, StreamListener

# Load Twitter API credentials
with open('auth_tokens.json') as f:
    auth_tokens = json.load(f)

# Kafka settings
kafka_bootstrap_servers = 'localhost:9092'
kafka_topic = 'twitter_stream'

# Setup Kafka producer
producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers)

# Twitter Stream Listener
class TweetStreamListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        tweet_text = tweet.get('text')
        producer.send(kafka_topic, tweet_text.encode('utf-8'))
        print(f'Sent tweet to Kafka: {tweet_text}')
        return True

    def on_error(self, status):
        print(f"Error: {status}")

# Setup Tweepy API
auth = OAuthHandler(auth_tokens['consumer_key'], auth_tokens['consumer_secret'])
auth.set_access_token(auth_tokens['access_token'], auth_tokens['access_token_secret'])
api = Stream(auth, TweetStreamListener())

# Start streaming tweets related to "CompanyX"
api.filter(track=['CompanyX'])
