import os
from sqlalchemy import inspect
from src.database.database import init_db, engine, Base

def database_exists():
    """بررسی می‌کند که آیا دیتابیس `newsbot.db` از قبل وجود دارد یا نه."""
    return os.path.exists("newsbot.db")

def tables_exist():
    """بررسی می‌کند که آیا جداول `tweets` و `news` در دیتابیس ایجاد شده‌اند یا نه."""
    inspector = inspect(engine)
    return "tweets" in inspector.get_table_names() and "news" in inspector.get_table_names()

def setup_database():
    """اگر دیتابیس وجود نداشته باشد، آن را می‌سازد. اگر جداول وجود نداشته باشند، آن‌ها را اضافه می‌کند."""
    if not database_exists():
        print("📦 دیتابیس وجود ندارد. در حال ایجاد دیتابیس و جداول...")
        init_db()
        print("✅ دیتابیس و جداول ایجاد شدند.")
    elif not tables_exist():
        print("⚠️ دیتابیس وجود دارد اما جداول `tweets` و `news` ناقص هستند. در حال اصلاح...")
        Base.metadata.create_all(engine)
        print("✅ جداول `tweets` و `news` اضافه شدند.")
    else:
        print("✅ دیتابیس و جداول از قبل موجود هستند.")

if __name__ == "__main__":
    setup_database()
