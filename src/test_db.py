# src/test_db.py
from models import session, Post

# ایجاد یک نمونه تستی از یک خبر
test_post = Post(
    type='news',
    source='https://www.ict.gov.ir/Components/NewsAgency/View/Rss.aspx',
    title='خبر تستی',
    content='این یک متن تستی برای خبر است.',
    summary='خلاصه‌ای از خبر تستی.',
    url='https://example.com/article',
    category='سیاسی',
    metadata={"views": 100, "likes": 20}
)

# ذخیره داده در دیتابیس
session.add(test_post)
session.commit()

# بازیابی و نمایش اطلاعات ذخیره شده
retrieved_post = session.query(Post).first()
print(f"✅ پست ذخیره شد: {retrieved_post.title}, منبع: {retrieved_post.source}")
