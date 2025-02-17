# src/fetchers/rss_fetcher.py
import feedparser
from datetime import datetime
from src.models import session, Post

def fetch_rss_feed(feed_url):
    """دریافت و پردازش فید RSS"""
    feed = feedparser.parse(feed_url)
    if 'entries' not in feed:
        print(f"❌ خطا در دریافت فید: {feed_url}")
        return

    for entry in feed.entries:
        # بررسی وجود داده‌های ضروری
        title = entry.get('title', 'بدون عنوان')
        link = entry.get('link', None)
        summary = entry.get('summary', '')
        published = entry.get('published_parsed')

        # تبدیل تاریخ انتشار به فرمت datetime
        timestamp = datetime(*published[:6]) if published else datetime.utcnow()

        # ذخیره در دیتابیس
        new_post = Post(
            type='news',
            source=feed_url,
            title=title,
            content=summary,
            summary=summary,
            url=link,
            timestamp=timestamp,
            category='اخبار'
        )

        # بررسی وجود پست تکراری
        exists = session.query(Post).filter_by(url=link).first()
        if not exists:
            session.add(new_post)
            print(f"✅ خبر ذخیره شد: {title}")

    session.commit()

# تست با یک فید خبری
if __name__ == "__main__":
    test_feed = "https://www.ict.gov.ir/Components/NewsAgency/View/Rss.aspx"
    fetch_rss_feed(test_feed)
