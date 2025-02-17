import threading
import time
from src.scheduler import start_scheduler
from src.config import load_config

# بارگذاری تنظیمات
config = load_config()
FETCH_INTERVAL = config["fetch_interval"]

def main():
    """
    اجرای سیستم پایش توییت‌ها و اخبار به صورت خودکار
    """
    print("🚀 راه‌اندازی سیستم پایش خودکار...")

    # اجرای زمان‌بندی در یک ترد جداگانه
    start_scheduler()

    # نگه داشتن برنامه در حال اجرا
    try:
        while True:
            time.sleep(FETCH_INTERVAL)
    except KeyboardInterrupt:
        print("\n⏹ توقف سیستم پایش.")

if __name__ == "__main__":
    main()
