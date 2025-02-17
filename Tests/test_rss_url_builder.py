import unittest
from src.fetchers.rss_url_builder import RSSURLBuilder

class TestRSSURLBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = RSSURLBuilder(base_url="https://nitter.net")

    def test_from_username(self):
        """
        بررسی تولید لینک RSS برای یک کاربر
        """
        url = self.builder.from_username("elonmusk")
        expected_url = "https://nitter.net/elonmusk/rss"
        self.assertEqual(url, expected_url)

    def test_from_hashtag(self):
        """
        بررسی تولید لینک RSS برای یک هشتگ
        """
        url = self.builder.from_hashtag("AI")
        expected_url = "https://nitter.net/hashtag/AI/rss"
        self.assertEqual(url, expected_url)

    def test_from_search(self):
        """
        بررسی تولید لینک RSS برای یک جست‌وجو
        """
        url = self.builder.from_search("OpenAI")
        expected_url = "https://nitter.net/search?f=tweets&q=OpenAI&rss=1"
        self.assertEqual(url, expected_url)

    def test_empty_username(self):
        """
        بررسی خطای ورودی خالی برای نام کاربری
        """
        with self.assertRaises(ValueError):
            self.builder.from_username("")

    def test_empty_hashtag(self):
        """
        بررسی خطای ورودی خالی برای هشتگ
        """
        with self.assertRaises(ValueError):
            self.builder.from_hashtag("")

    def test_empty_search(self):
        """
        بررسی خطای ورودی خالی برای جست‌وجو
        """
        with self.assertRaises(ValueError):
            self.builder.from_search("")

if __name__ == '__main__':
    unittest.main()
