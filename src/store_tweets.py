from src.fetchers.tweet_fetcher import TweetFetcher
from src.database.database import save_tweet, SessionLocal


def fetch_and_store_tweets(rss_url, max_tweets=5):
    """
    دریافت و ذخیره توییت‌ها از Nitter RSS
    """
    print(f"📡 دریافت توییت‌ها از: {rss_url}")

    # دریافت توییت‌ها از Nitter
    fetcher = TweetFetcher(rss_url)
    tweets = fetcher.fetch_tweets(max_tweets=max_tweets)

    # ذخیره در دیتابیس
    db = SessionLocal()
    for tweet in tweets:
        tweet_data = {
            "tweet_id": tweet["tweet_id"],
            "username": tweet["username"],
            "text": tweet["text"],
            "likes": tweet["likes"],
            "retweets": tweet["retweets"],
            "replies": tweet["replies"],
            "quotes": tweet["quotes"],
            "pubDate": tweet["pubDate"],
            "link": tweet["link"]
        }
        save_tweet(db, tweet_data)
    db.close()

    print("✅ ذخیره‌سازی توییت‌ها کامل شد.")


# اگر این فایل مستقیماً اجرا شد، تست دستی انجام بده
if __name__ == "__main__":
    test_rss_url = "http://46.249.98.217:8080/elonmusk/rss"
    fetch_and_store_tweets(test_rss_url, max_tweets=3)
