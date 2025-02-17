import time
import threading
import random
import json
import urllib.parse
from src.store_tweets import fetch_and_store_tweets
from src.config import NITTER_SERVERS, SEARCH_QUERIES, FETCH_INTERVAL, MAX_RETRIES, RETRY_INTERVAL

def get_nitter_server():
    """انتخاب تصادفی یک سرور Nitter برای توزیع بار و مدیریت Failover"""
    return random.choice(NITTER_SERVERS)

def build_nitter_url(server, search_query):
    """ساخت URL معتبر برای دریافت داده از Nitter"""
    encoded_query = urllib.parse.quote_plus(search_query)  # تبدیل فضای خالی به %20
    return f"{server}/search/rss?f=tweets&q={encoded_query}"

def scheduled_task():
    """اجرای جمع‌آوری داده‌ها به صورت مستمر"""
    while True:
        print("⏳ شروع پردازش داده‌ها...")
        for query in SEARCH_QUERIES:
            success = False
            for attempt in range(MAX_RETRIES):
                server = get_nitter_server()
                rss_url = build_nitter_url(server, query)

                try:
                    print(f"📡 دریافت توییت‌ها از: {rss_url}")
                    fetch_and_store_tweets(rss_url, query)
                    success = True
                    break  # اگر موفق شد، دیگر نیازی به تلاش مجدد نیست
                except Exception as e:
                    print(f"❌ خطا در دریافت داده برای '{query}' از {server}: {e}")
                    time.sleep(RETRY_INTERVAL)  # صبر قبل از تلاش مجدد

            if not success:
                print(f"⚠️ عدم موفقیت در دریافت داده برای '{query}' پس از {MAX_RETRIES} تلاش!")

        print(f"✅ پردازش کامل شد. زمان‌بندی بعدی در {FETCH_INTERVAL} ثانیه...")
        time.sleep(FETCH_INTERVAL)  # صبر تا اجرای بعدی

def start_scheduler():
    """اجرای زمان‌بندی در یک ترد جداگانه برای جلوگیری از بلاک شدن برنامه"""
    scheduler_thread = threading.Thread(target=scheduled_task, daemon=True)
    scheduler_thread.start()
