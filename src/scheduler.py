import time
import threading
import random
from src.utils.url_builder import build_nitter_url
from src.store_tweets import fetch_and_store_tweets
from src.config import NITTER_SERVERS, SEARCH_QUERIES, FETCH_INTERVAL, MAX_RETRIES, RETRY_INTERVAL

def get_nitter_server():
    """انتخاب تصادفی یک سرور Nitter برای توزیع بار و مدیریت Failover"""
    return random.choice(NITTER_SERVERS)

def scheduled_task():
    """اجرای جمع‌آوری داده‌ها به صورت مستمر"""
    while True:
        print("⏳ شروع پردازش داده‌ها...")
        for query in SEARCH_QUERIES:
            success = False
            for attempt in range(MAX_RETRIES):
                server = get_nitter_server()
                rss_url = build_nitter_url(server, query)  # ✅ حالا کوئری درست ساخته می‌شود.

                try:
                    print(f"📡 دریافت توییت‌ها از: {rss_url}")
                    fetch_and_store_tweets(rss_url, query)  # ✅ ارسال `search_query`
                    success = True
                    break
                except Exception as e:
                    print(f"❌ خطا در دریافت داده برای '{query}' از {server}: {e}")
                    time.sleep(RETRY_INTERVAL)

            if not success:
                print(f"⚠️ عدم موفقیت در دریافت داده برای '{query}' پس از {MAX_RETRIES} تلاش!")

        print(f"✅ پردازش کامل شد. زمان‌بندی بعدی در {FETCH_INTERVAL} ثانیه...")
        time.sleep(FETCH_INTERVAL)

def start_scheduler():
    """اجرای زمان‌بندی در یک ترد جداگانه برای جلوگیری از بلاک شدن برنامه"""
    scheduler_thread = threading.Thread(target=scheduled_task, daemon=True)
    scheduler_thread.start()
