from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# 📌 تنظیم پایگاه داده (SQLite، قابل تغییر به PostgreSQL یا MySQL)
DATABASE_URL = "sqlite:///newsbot.db"

# 📌 ایجاد موتور پایگاه داده
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 📌 تعریف مدل پایه
Base = declarative_base()

# 📌 مدل توییت‌ها
class Tweet(Base):
    """مدل دیتابیس برای ذخیره توییت‌ها"""
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    likes = Column(Integer, default=0)
    retweets = Column(Integer, default=0)
    replies = Column(Integer, default=0)
    quotes = Column(Integer, default=0)
    pub_date = Column(DateTime, default=datetime.datetime.utcnow)
    link = Column(String, nullable=False)

# 📌 مدل اخبار
class News(Base):
    """مدل دیتابیس برای ذخیره اخبار"""
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    source = Column(String, nullable=False)  # منبع خبر، مثلا "BBC" یا "CNN"
    content = Column(Text, nullable=False)  # متن خبر
    category = Column(String, nullable=True)  # مثلا 'tech', 'politics'
    pub_date = Column(DateTime, default=datetime.datetime.utcnow)
    url = Column(String, unique=True, nullable=False)

# 📌 مقداردهی اولیه دیتابیس
def init_db():
    """ایجاد جداول دیتابیس در صورت عدم وجود"""
    Base.metadata.create_all(bind=engine)

# 📌 تابع دریافت اتصال به دیتابیس
def get_db():
    """مدیریت اتصال به پایگاه داده"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 📌 تابع ذخیره توییت‌ها
def save_tweet(db, tweet_data):
    """
    ذخیره توییت در پایگاه داده (در صورت عدم وجود)
    """
    existing_tweet = db.query(Tweet).filter(Tweet.tweet_id == tweet_data["tweet_id"]).first()
    if existing_tweet:
        print(f"⚠️ توییت با ID {tweet_data['tweet_id']} قبلاً ذخیره شده است.")
        return None  # جلوگیری از ذخیره‌سازی تکراری

    new_tweet = Tweet(
        tweet_id=tweet_data["tweet_id"],
        username=tweet_data["username"],
        text=tweet_data["text"],
        likes=tweet_data["likes"],
        retweets=tweet_data["retweets"],
        replies=tweet_data["replies"],
        quotes=tweet_data["quotes"],
        pub_date=tweet_data["pubDate"],
        link=tweet_data["link"]
    )
    db.add(new_tweet)
    db.commit()
    db.refresh(new_tweet)
    print(f"✅ توییت {tweet_data['tweet_id']} ذخیره شد.")
    return new_tweet

# 📌 تابع ذخیره اخبار
def save_news(db, news_data):
    """
    ذخیره خبر در پایگاه داده (در صورت عدم وجود)
    """
    existing_news = db.query(News).filter(News.url == news_data["url"]).first()
    if existing_news:
        print(f"⚠️ خبر با لینک {news_data['url']} قبلاً ذخیره شده است.")
        return None  # جلوگیری از ذخیره‌سازی تکراری

    new_news = News(
        title=news_data["title"],
        source=news_data["source"],
        content=news_data["content"],
        category=news_data.get("category", None),  # مقدار پیش‌فرض None
        pub_date=news_data["pub_date"],
        url=news_data["url"]
    )
    db.add(new_news)
    db.commit()
    db.refresh(new_news)
    print(f"✅ خبر {news_data['url']} ذخیره شد.")
    return new_news
