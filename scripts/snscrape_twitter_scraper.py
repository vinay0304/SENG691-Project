import json
import snscrape.modules.twitter as sntwitter
import time

# Load Twitter scraping configurations
with open('../config/twitter_scrape_config.json') as f:
    scrape_config = json.load(f)

# Twitter scraping settings
search_query = 'CompanyX'
max_tweets = scrape_config.get('max_tweets', 100)

# Scraping loop
tweets = []
for tweet in sntwitter.TwitterSearchScraper(f'{search_query} since:{scrape_config["start_date"]}').get_items():
    tweets.append(tweet.content)
    if len(tweets) >= max_tweets:
        break
    time.sleep(1)  # Add a delay to avoid being rate-limited

# Print and process tweets (modify as needed)
for tweet_text in tweets:
    print(f'Scraped tweet: {tweet_text}')
    # Process the tweet (e.g., send it to Kafka for analysis)