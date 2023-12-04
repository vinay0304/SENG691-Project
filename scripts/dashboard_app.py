
from flask import Flask, render_template, jsonify
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from textblob import TextBlob

app = Flask(__name__)

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
sentiments = tweets.map(lambda tweet: TextBlob(tweet).sentiment.polarity)

# Aggregate sentiments every 10 minutes
windowed_sentiments = sentiments.window(windowDuration=600, slideDuration=10)
aggregated_sentiments = windowed_sentiments.reduce(lambda x, y: x + y)

# Store aggregated sentiments in a global variable for web access
global_aggregated_sentiments = 0.0
aggregated_sentiments.foreachRDD(lambda time, rdd: global_aggregated_sentiments = rdd.collect()[0])

# Define a route to render the dashboard
@app.route('/')
def dashboard():
    return render_template('dashboard.html', sentiment_score=global_aggregated_sentiments)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
