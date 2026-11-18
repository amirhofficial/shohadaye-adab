from django.shortcuts import render
from django.urls import NoReverseMatch, reverse


def _safe_reverse(name, fallback="#"):
    """آدرس را برمی‌گرداند؛ اگر مسیر با این نام وجود نداشت، مقدار جایگزین."""
    try:
        return reverse(name)
    except NoReverseMatch:
        return fallback


# ---------------------------------------------------------------------------
# PLACEHOLDER DATA — نمونه‌اند و خبر/تصویر واقعی مدرسه نیستند.
# وقتی مدل‌های اپ‌های school / gallery / achievements را بررسی کردیم،
# این لیست‌ها با کوئری واقعی جایگزین می‌شوند.
# ---------------------------------------------------------------------------
PLACEHOLDER_NEWS = [
    {
        "title": "عنوان نمونه برای یک اطلاعیه آموزشی",
        "summary": "این متن فقط برای نمایش چیدمان است و با خلاصهٔ واقعی خبر جایگزین می‌شود.",
        "category": "اطلاعیه",
        "date": "۱۴۰۴/۰۰/۰۰",
        "image": "images/news/news-1.jpg",
        "image_alt": "تصویر خبر نمونه ۱",
        "url": "#",
        "is_placeholder": True,
    },
    {
        "title": "عنوان نمونه برای خبر یک مراسم یا رویداد",
        "summary": "این متن فقط برای نمایش چیدمان است و با خلاصهٔ واقعی خبر جایگزین می‌شود.",
        "category": "رویداد",
        "date": "۱۴۰۴/۰۰/۰۰",
        "image": "images/news/news-2.jpg",
        "image_alt": "تصویر خبر نمونه ۲",
        "url": "#",
        "is_placeholder": True,
    },
    {
        "title": "عنوان نمونه برای خبر یک موفقیت دانش‌آموزی",
        "summary": "این متن فقط برای نمایش چیدمان است و با خلاصهٔ واقعی خبر جایگزین می‌شود.",
        "category": "افتخارات",
        "date": "۱۴۰۴/۰۰/۰۰",
        "image": "images/news/news-3.jpg",
        "image_alt": "تصویر خبر نمونه ۳",
        "url": "#",
        "is_placeholder": True,
    },
]

# stat=None یعنی هنوز آمار تأییدشده‌ای ثبت نشده است (عدد جعلی نمایش داده نمی‌شود).
ACHIEVEMENT_CATEGORIES = [
    {"title": "علمی", "icon": "flask", "stat": None},
    {"title": "فرهنگی", "icon": "landmark", "stat": None},
    {"title": "ورزشی", "icon": "trophy", "stat": None},
    {"title": "هنری", "icon": "palette", "stat": None},
]

PLACEHOLDER_GALLERY = [
    {"title": "محیط مدرسه", "image": "images/gallery/environment.jpg", "url": "#"},
    {"title": "فعالیت‌های آموزشی", "image": "images/gallery/education.jpg", "url": "#"},
    {"title": "مراسم و رویدادها", "image": "images/gallery/events.jpg", "url": "#"},
    {"title": "پروژه‌های دانش‌آموزی", "image": "images/gallery/projects.jpg", "url": "#"},
    {"title": "فرهنگی و ورزشی", "image": "images/gallery/activities.jpg", "url": "#"},
]


def home(request):
    context = {
        # فقط اگر مسیری با نام «login» وجود داشته باشد استفاده می‌شود؛ مسیر جدید ساخته نشده است.
        "student_panel_url": _safe_reverse("login", "#student-panel"),
        "schedule_url": "#schedule",
        "homework_url": "#homework",
        "about_url": "#about",
        "news_list_url": "#news",
        "achievements_url": "#achievements",
        "gallery_url": "#gallery",
        "search_endpoint": "",  # بعداً: reverse("search")
        "news_items": PLACEHOLDER_NEWS,
        "achievement_categories": ACHIEVEMENT_CATEGORIES,
        "gallery_items": PLACEHOLDER_GALLERY,
    }
    return render(request, "home.html", context)
