# src/models.py
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# تعریف کلاس پایه برای مدل‌های SQLAlchemy
Base = declarative_base()

class Post(Base):
    """مدل پایگاه داده برای ذخیره اخبار و توییت‌ها"""
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(10), nullable=False)  # 'news' یا 'tweet'
    source = Column(String(255), nullable=False)
    title = Column(String(255))
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    url = Column(String(255))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    category = Column(String(100), nullable=True)
    extra_metadata = Column(JSON, nullable=True)  # تغییر نام فیلد

# تابع راه‌اندازی پایگاه داده
def init_db(db_url='sqlite:///newsbot.db'):
    """ایجاد پایگاه داده و جدول‌ها"""
    engine = create_engine(db_url, echo=True)
    Base.metadata.create_all(engine)
    return engine

# تنظیم session برای تعامل با پایگاه داده
engine = init_db()
Session = sessionmaker(bind=engine)
session = Session()
