class RSSURLBuilder:
    def __init__(self, base_url="http://46.249.98.217:8080"):
        """
        کلاس تولید لینک‌های RSS برای دریافت توییت‌ها از Nitter
        :param base_url: آدرس سرور Nitter (قابل تغییر در صورت نیاز)
        """
        self.base_url = base_url

    def from_username(self, username):
        """
        تولید لینک RSS برای دریافت توییت‌های یک کاربر خاص
        :param username: نام کاربری توییتر (بدون @)
        :return: لینک RSS برای کاربر
        """
        if not username:
            raise ValueError("نام کاربری نباید خالی باشد.")
        return f"{self.base_url}/{username}/rss"

    def from_hashtag(self, hashtag):
        """
        تولید لینک RSS برای دریافت توییت‌های یک هشتگ خاص
        :param hashtag: هشتگ بدون #
        :return: لینک RSS برای هشتگ
        """
        if not hashtag:
            raise ValueError("هشتگ نباید خالی باشد.")
        return f"{self.base_url}/hashtag/{hashtag}/rss"

    def from_search(self, query):
        """
        تولید لینک RSS برای دریافت توییت‌های مرتبط با یک جست‌وجو
        :param query: عبارت جست‌وجو
        :return: لینک RSS برای جست‌وجو
        """
        if not query:
            raise ValueError("عبارت جست‌وجو نباید خالی باشد.")
        return f"{self.base_url}/search?f=tweets&q={query}&rss=1"
