# src/fetchers/tweet_fetcher.py
import requests
from datetime import datetime
from src.models import session, Post

# URL سرور Nitter (در صورت خرابی، از سرور جایگزین استفاده کنید)
NITTER_URL = "https://nitter.net"

def fetch_tweets(username, count=5):
    """دریافت توییت‌های یک کاربر از Nitter"""
    url = f"{NITTER_URL}/{username}/rss"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"❌ خطا در دریافت توییت‌ها از {username}: {response.status_code}")
        return

    feed = response.text

    # پردازش و استخراج توییت‌ها
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(feed, 'xml')
    items = soup.find_all('item')[:count]

    for item in items:
        title = item.title.text
        link = item.link.text
        description = item.description.text
        pub_date = item.pubDate.text

        # تبدیل تاریخ
        timestamp = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %Z')

        # بررسی تکراری نبودن توییت
        exists = session.query(Post).filter_by(url=link).first()
        if exists:
            continue

        # ذخیره در دیتابیس
        new_post = Post(
            type='tweet',
            source=username,
            title=title,
            content=description,
            summary=description[:150],  # خلاصه ۱۵۰ کاراکتری
            url=link,
            timestamp=timestamp,
            category='توییتر'
        )

        session.add(new_post)
        print(f"✅ توییت ذخیره شد: {title}")

    session.commit()

# تست با یک کاربر توییتر
if __name__ == "__main__":
    test_username = "elonmusk"
    fetch_tweets(test_username)
