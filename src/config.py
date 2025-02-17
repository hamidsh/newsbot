import json
from pathlib import Path

# دریافت مسیر فایل کانفیگ
CONFIG_PATH = Path(__file__).parent.parent / "config.json"

def load_config():
    """بارگذاری تنظیمات از `config.json`"""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        print(f"⚠️ هشدار: فایل پیکربندی `{CONFIG_PATH}` یافت نشد! از مقادیر پیش‌فرض استفاده می‌شود.")
        return {}

# بارگذاری تنظیمات
CONFIG = load_config()

# **پیکربندی سرورهای Nitter و جستجو**
NITTER_SERVERS = CONFIG.get("nitter_servers", ["http://46.249.98.217:8080"])
SEARCH_QUERIES = CONFIG.get("search_queries", [])
FETCH_INTERVAL = int(CONFIG.get("fetch_interval", 600))
MAX_RETRIES = int(CONFIG.get("max_retries", 3))
RETRY_INTERVAL = int(CONFIG.get("retry_interval", 300))

# **پیکربندی پایگاه داده**
DATABASE_URL = CONFIG.get("DATABASE_URL", "sqlite:///newsbot.db")
MAX_TWEETS = int(CONFIG.get("MAX_TWEETS", 5))

# **چاپ وضعیت تنظیمات برای بررسی صحت بارگذاری**
print(f"📌 تنظیمات بارگذاری شد: Nitter Servers = {NITTER_SERVERS}, Max Tweets = {MAX_TWEETS}, DB = {DATABASE_URL}")
