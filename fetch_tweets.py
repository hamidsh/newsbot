from src.fetchers.tweet_fetcher import TweetFetcher
import json

# 📌 آدرس RSS برای یوزرنیم خاص (مثلاً elonmusk)
rss_url = "http://46.249.98.217:8080/elonmusk/rss"
fetcher = TweetFetcher(rss_url)

# 📌 دریافت توییت‌ها
tweets = fetcher.fetch_tweets(max_tweets=5)

# 📌 نمایش خروجی JSON در کنسول
print(json.dumps(tweets, indent=4, ensure_ascii=False))

