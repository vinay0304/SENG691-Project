import json
from kafka import KafkaConsumer
from pymongo import MongoClient

# MongoDB settings
mongo_uri = 'mongodb+srv://sengapp:<XM4uJ0fxAG5w2OgR>@cluster0.zxoginc.mongodb.net/'
mongo_collection = 'tweets'

# Setup MongoDB client
client = MongoClient(mongo_uri)
db = client.get_database()
collection = db[mongo_collection]

# Kafka settings
kafka_bootstrap_servers = 'localhost:9092'
kafka_topic = 'twitter_stream'

# Setup Kafka consumer
consumer = KafkaConsumer(kafka_topic, bootstrap_servers=[kafka_bootstrap_servers])

# Consume and persist tweets to MongoDB
for message in consumer:
    tweet_text = message.value.decode('utf-8')
    tweet = {'text': tweet_text}
    collection.insert_one(tweet)
    print(f'Persisted tweet to MongoDB: {tweet_text}')
