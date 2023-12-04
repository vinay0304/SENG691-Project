from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from textblob import TextBlob

# Setup Spark session
spark = SparkSession.builder.appName('TwitterSentimentAnalysis').getOrCreate()

# Setup Spark Streaming context
ssc = StreamingContext(spark.sparkContext, batchDuration=10)

# Kafka settings
kafka_bootstrap_servers = 'localhost:9092'
kafka_topic = 'twitter_stream'

# Create a direct stream from Kafka
kafka_stream = KafkaUtils.createDirectStream(ssc, [kafka_topic], {'metadata.broker.list': kafka_bootstrap_servers})

# Process the stream
tweets = kafka_stream.map(lambda x: x[1].decode('utf-8'))
from textblob import TextBlob

# Example text
text = "I love using TextBlob! It's a fantastic library."

# Create a TextBlob object
blob = TextBlob(text)

# Get sentiment polarity (ranges from -1 to 1)
sentiment_polarity = blob.sentiment.polarity

# Classify sentiment
if sentiment_polarity > 0:
    sentiment = "Positive"
elif sentiment_polarity < 0:
    sentiment = "Negative"
else:
    sentiment = "Neutral"

print(f"Sentiment: {sentiment}")

sentiments = tweets.map(lambda tweet: TextBlob(tweet).sentiment.polarity)

# Print sentiments to the console (you can modify this part for writing to Kafka or a database)
sentiments.pprint()

# Start the streaming context
ssc.start()
ssc.awaitTermination()
