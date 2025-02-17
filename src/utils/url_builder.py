import urllib.parse
from src.config import CONFIG


def build_nitter_url(base_url, search_query):
    """
    ساخت URL برای دریافت توییت‌ها از `Nitter`
    :param base_url: آدرس سرور `Nitter`
    :param search_query: عبارت جستجو
    :return: URL معتبر
    """
    use_recent = CONFIG.get("use_recent", False)

    encoded_query = urllib.parse.quote(search_query)  # ✅ تبدیل صحیح کاراکترهای ویژه

    if use_recent:
        return f"{base_url}/search/rss?f=tweets&q={encoded_query}&sort_order=recency"  # ✅ تصحیح آدرس
    return f"{base_url}/search/rss?f=tweets&q={encoded_query}"  # ✅ تبدیل صحیح
