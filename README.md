# پروژه NewsBot

این پروژه با هدف جمع‌آوری اخبار از فیدهای RSS و توییت‌ها (از طریق Nitter یا روش مشابه) و ذخیره آن‌ها در یک پایگاه داده طراحی شده است. در ادامه، هدف پروژه، زیرساخت‌های استفاده‌شده، ساختار پروژه، طراحی دیتابیس و نقشه راه توسعه آورده شده است.

---

## 1. هدف پروژه

- **جمع‌آوری اخبار:**  
  دریافت اخبار از فیدهای RSS وب‌سایت‌های خبری.
  
- **جمع‌آوری توییت‌ها:**  
  دریافت توییت‌ها (با استفاده از Nitter یا روش‌های مشابه).

- **ذخیره‌سازی داده‌ها:**  
  ذخیره اخبار و توییت‌ها در یک دیتابیس یکپارچه (در مرحله اول از SQLite استفاده می‌شود و در آینده امکان مهاجرت به PostgreSQL یا MySQL وجود دارد).

- **ارسال بسته خبری:**  
  ارائه بسته‌های خبری به کاربران (فعلاً از طریق ربات تلگرام) به صورت دوره‌ای یا بر اساس درخواست.

---

## 2. زیرساخت‌ها و محیط اجرا

- **محیط توسعه (Local):**  
  - سیستم: ویندوز 11 (64 بیتی)
  - نسخه پایتون: 3.9 (یا نسخه معادل که در سرور نیز استفاده خواهد شد)
  - IDE: PyCharm (توصیه‌شده) یا هر ادیتور دیگر
  - ابزارهای مورد نیاز: Git، محیط مجازی (venv)

- **محیط سرور (Production):**  
  - سیستم: اوبونتو 24 روی سرور ابری
  - نسخه پایتون: همان نسخه استفاده‌شده در محیط توسعه
  - انتقال کد از طریق Git یا ابزارهای Deployment (مانند SFTP)

---

## 3. وضعیت نصب و راه‌اندازی (Local)

✅ **نصب پایتون 3.9** (نسخه 64 بیتی) روی ویندوز
✅ **نصب Git جهت کنترل نسخه**
✅ **ایجاد محیط مجازی**
✅ **مدیریت وابستگی‌ها و نصب پکیج‌های مورد نیاز**
✅ **راه‌اندازی Git در پروژه و اتصال به GitHub**

---

## 4. مدل پایگاه داده و ساختار داده‌ها

- مدل پایگاه داده به گونه‌ای طراحی شده که ذخیره‌سازی اخبار و توییت‌ها **در یک جدول یکپارچه** انجام شود.
- جدول `posts` دارای فیلدهای زیر است:
  - `id` (شناسه یکتا)
  - `type` (مشخص‌کننده نوع پست: 'news' یا 'tweet')
  - `source` (منبع دریافت داده مانند URL فید یا نام کاربری توییتر)
  - `title` (عنوان خبر یا توییت)
  - `content` (متن کامل محتوا)
  - `summary` (خلاصه محتوا)
  - `url` (لینک اصلی محتوا)
  - `timestamp` (زمان انتشار)
  - `category` (دسته‌بندی محتوا)
  - `extra_metadata` (ذخیره اطلاعات اضافی به صورت JSON برای امکان گسترش آینده)
- **مدل پایگاه داده با موفقیت پیاده‌سازی و تست شد**. داده‌های تستی بدون مشکل ذخیره و بازیابی شدند.
- پردازش و فیلترگذاری **در لایه جداگانه‌ای انجام خواهد شد** تا بهینه‌سازی الگوریتم‌ها در آینده آسان باشد.

---

## 5. ساختار پیشنهادی پروژه

```
newsbot/
├── venv/                 # محیط مجازی (Local)
├── src/
│   ├── __init__.py
│   ├── config.py         # تنظیمات کلی پروژه (مسیر دیتابیس، اطلاعات اتصال و ...)
│   ├── db.py             # مدیریت اتصال به دیتابیس و ایجاد Session
│   ├── models.py         # تعریف مدل دیتابیس (مثلاً مدل Post)
│   ├── fetchers/         # ماژول‌های دریافت داده (RSS، توییت‌ها و ...)
│   │   ├── __init__.py
│   │   ├── rss_fetcher.py    # دریافت و نرمالایز کردن اخبار از RSS
│   │   └── tweet_fetcher.py  # دریافت توییت‌ها (از Nitter یا API توییتر)
│   ├── news_package.py   # منطق ساخت بسته خبری (ترکیب و فیلتر کردن پست‌ها)
│   └── telegram_bot/     # ماژول‌های مرتبط با ربات تلگرام
├── tests/                # تست‌های واحد و یکپارچه
│   └── test_models.py
├── requirements.txt
└── README.md
```

---

## 6. روند پیشرفت پروژه و هماهنگی بین مراحل توسعه

✅ **ایجاد پروژه در PyCharm و تنظیمات اولیه**
✅ **اتصال پروژه به GitHub و راه‌اندازی Git**
✅ **بررسی مدل‌های پیشنهادی و انتخاب رویکرد نهایی توسعه**
✅ **پیاده‌سازی مدل پایگاه داده (`models.py`) و تست موفق**
✅ **ایجاد و تست ماژول دریافت اخبار از RSS (`rss_fetcher.py`)**
⬜ **ایجاد و تست ماژول دریافت توییت‌ها از Nitter (`tweet_fetcher.py`)**
⬜ **پیاده‌سازی و تست ماژول بسته خبری (`news_package.py`)**
⬜ **ایجاد و تست ربات تلگرام (`telegram_bot/`)**
⬜ **انتقال کد به سرور اوبونتو و راه‌اندازی تولیدی (Production)**

- **پس از هر مرحله، سوالی برای تأیید نهایی از کاربر پرسیده خواهد شد.**
- **در صورت تأیید، اطلاعات پروژه و مرحله فعلی در این فایل به‌روز خواهد شد.**
- **اگر مشکلی در هر مرحله پیش بیاید، چالش‌ها و مشکلات ثبت خواهند شد تا فراموش نشوند و حل شوند.**

---

## 7. نتیجه‌گیری

این پروژه به صورت ماژولار طراحی شده تا هر بخش (مدل دیتابیس، دریافت اخبار و توییت‌ها، ربات تلگرام، بسته‌بندی اخبار و زمان‌بندی) به صورت مستقل توسعه، تست و بهبود یابد. هدف نهایی، ایجاد سیستمی یکپارچه و قابل توسعه برای جمع‌آوری و ارسال اخبار به کاربران است.

---

*تاریخ آخرین به‌روزرسانی: [تاریخ به‌روزرسانی]*  
*در صورت بروز تغییرات یا تصمیمات جدید، این فایل به‌روز خواهد شد.*

