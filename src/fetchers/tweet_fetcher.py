import feedparser
import re
from bs4 import BeautifulSoup

class TweetFetcher:
    def __init__(self, rss_url):
        """
        دریافت و پردازش توییت‌ها از یک آدرس RSS (ورودی باید لینک فید باشد)
        :param rss_url: لینک RSS از سرور Nitter
        """
        self.rss_url = rss_url

    def extract_stats(self, description):
        """
        استخراج آمار لایک، ریتوییت، ریپلای و کوت‌ها از متن توییت
        """
        stats_pattern = re.compile(r"❤️ Likes: (\d+) 🔁 Retweets: (\d+) 💬 Replies: (\d+) 🗨 Quotes: (\d+)")
        match = stats_pattern.search(description)
        if match:
            return {
                "likes": int(match.group(1)),
                "retweets": int(match.group(2)),
                "replies": int(match.group(3)),
                "quotes": int(match.group(4))
            }
        return {"likes": 0, "retweets": 0, "replies": 0, "quotes": 0}

    def fetch_tweets(self, max_tweets=10):
        """
        دریافت و پردازش توییت‌ها از RSS
        :param max_tweets: تعداد حداکثر توییت‌ها برای پردازش
        :return: لیست دیکشنری شامل اطلاعات توییت‌ها
        """
        feed = feedparser.parse(self.rss_url)

        tweets = []
        for entry in feed.entries[:max_tweets]:
            stats = self.extract_stats(entry.description)
            soup = BeautifulSoup(entry.description, "html.parser")
            clean_text = soup.get_text()

            tweet_match = re.search(r"status/(\d+)", entry.link)
            tweet_id = tweet_match.group(1) if tweet_match else None
            modified_link = f"https://x.com/i/web/status/{tweet_id}" if tweet_id else entry.link

            tweets.append({
                "title": entry.title,
                "username": entry.author if "author" in entry else None,
                "text": clean_text.strip(),
                "likes": stats["likes"],
                "retweets": stats["retweets"],
                "replies": stats["replies"],
                "quotes": stats["quotes"],
                "pubDate": entry.published,
                "tweet_id": tweet_id,
                "link": modified_link
            })

        return tweets
