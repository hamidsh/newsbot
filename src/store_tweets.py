from src.fetchers.tweet_fetcher import TweetFetcher
from src.database.database import save_tweet, SessionLocal
from datetime import datetime
import email.utils
import re


def clean_text(text):
    """حذف تگ‌های HTML و نرمال‌سازی متن توییت"""
    clean = re.sub(r"<.*?>", "", text)
    return clean.strip()


def fetch_and_store_tweets(rss_url):
    """
    دریافت و ذخیره توییت‌ها از آدرس RSS مشخص‌شده
    :param rss_url: لینک فید RSS برای دریافت توییت‌ها
    """
    print(f"📡 دریافت توییت‌ها از: {rss_url}")

    fetcher = TweetFetcher(rss_url)
    tweets = fetcher.fetch_tweets()

    db = SessionLocal()
    for tweet in tweets:
        try:
            pub_date_tuple = email.utils.parsedate_tz(tweet["pubDate"])
            pub_date = datetime(*pub_date_tuple[:6]) if pub_date_tuple else datetime.utcnow()

            tweet_data = {
                "tweet_id": str(tweet.get("tweet_id", "")),
                "username": str(tweet.get("username", "")),
                "text": clean_text(tweet.get("text", "")),
                "likes": int(tweet.get("likes", 0)),
                "retweets": int(tweet.get("retweets", 0)),
                "replies": int(tweet.get("replies", 0)),
                "quotes": int(tweet.get("quotes", 0)),
                "pubDate": pub_date,
                "link": str(tweet.get("link", ""))
            }
            save_tweet(db, tweet_data)
        except Exception as e:
            print(f"❌ خطا در پردازش توییت {tweet.get('tweet_id', 'N/A')}: {e}")

    db.close()
    print("✅ ذخیره‌سازی توییت‌ها کامل شد.")


# اجرای مستقل تست با مقدار پیش‌فرض
# if __name__ == "__main__":
#     test_rss_url = "http://46.249.98.217:8080/elonmusk/rss"  # مقدار پیش‌فرض برای تست
#     fetch_and_store_tweets(test_rss_url)
