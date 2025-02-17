import json
import os

# دریافت مسیر فایل کانفیگ
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.json")

# تابعی برای خواندن تنظیمات از `config.json`
def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

# بارگذاری تنظیمات
CONFIG = load_config()

# تعریف متغیرهای سراسری
RSS_URL = CONFIG.get("RSS_URL", "http://46.249.98.217:8080")
MAX_TWEETS = CONFIG.get("MAX_TWEETS", 5)
DATABASE_URL = CONFIG.get("DATABASE_URL", "sqlite:///newsbot.db")
