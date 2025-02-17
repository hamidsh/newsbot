import time
import threading
import random
import json
from src.store_tweets import fetch_and_store_tweets
from src.config import DATABASE_URL

# بارگذاری پیکربندی
with open("config.json", "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

NITTER_SERVERS = config.get("nitter_servers", ["http://46.249.98.217:8080"])
SEARCH_QUERIES = config.get("search_queries", [])
FETCH_INTERVAL = config.get("fetch_interval", 600)
MAX_RETRIES = config.get("max_retries", 3)
RETRY_INTERVAL = config.get("retry_interval", 300)

def get_nitter_server():
    """انتخاب تصادفی یک سرور Nitter برای توزیع بار و مدیریت Failover"""
    return random.choice(NITTER_SERVERS)

def scheduled_task():
    """اجرای جمع‌آوری داده‌ها به صورت زمان‌بندی شده"""
    print("⏳ شروع پردازش داده‌ها...")
    for query in SEARCH_QUERIES:
        server = get_nitter_server()
        rss_url = f"{server}/search/rss?f=tweets&q={query}"
        success = False

        for attempt in range(MAX_RETRIES):
            try:
                fetch_and_store_tweets(rss_url, query)
                success = True
                break  # اگر موفق شد، ادامه ندهد
            except Exception as e:
                print(f"❌ خطا در دریافت داده برای '{query}' از {server}: {e}")
                time.sleep(RETRY_INTERVAL)  # صبر قبل از تلاش مجدد

        if not success:
            print(f"⚠️ عدم موفقیت در دریافت داده برای '{query}' پس از {MAX_RETRIES} تلاش!")

    print(f"✅ پردازش کامل شد. زمان‌بندی بعدی در {FETCH_INTERVAL} ثانیه...")
    time.sleep(FETCH_INTERVAL)

def start_scheduler():
    """اجرای زمان‌بندی در یک ترد جداگانه برای جلوگیری از بلاک شدن برنامه"""
    scheduler_thread = threading.Thread(target=scheduled_task, daemon=True)
    scheduler_thread.start()
