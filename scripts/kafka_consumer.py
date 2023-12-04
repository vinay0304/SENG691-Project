from kafka import KafkaConsumer

consumer = KafkaConsumer('twitter_stream', bootstrap_servers=['localhost:9092'])

# Process the tweet send it to Spark for analysis
for message in consumer:
    tweet_text = message.value.decode('utf-8')
    print(f'Received tweet: {tweet_text}')
    
