import unittest
from src.fetchers.tweet_fetcher import TweetFetcher

class TestTweetFetcher(unittest.TestCase):
    def setUp(self):
        # نمونه لینک از یک یوزرنیم (در صورت تغییر سرور Nitter، لینک را تغییر دهید)
        self.test_rss_url = "http://46.249.98.217:8080/elonmusk/rss"
        self.fetcher = TweetFetcher(self.test_rss_url)

    def test_fetch_tweets(self):
        """
        بررسی دریافت توییت‌های یوزرنیم مشخص‌شده
        """
        tweets = self.fetcher.fetch_tweets(max_tweets=5)
        self.assertIsInstance(tweets, list)
        self.assertGreater(len(tweets), 0)
        self.assertIn("username", tweets[0])
        self.assertIn("text", tweets[0])
        self.assertIn("link", tweets[0])

if __name__ == '__main__':
    unittest.main()
