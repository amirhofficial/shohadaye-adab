
from django.db import models


class SchoolSetting(models.Model):
    name = models.CharField(
        max_length=150,
        default='مدرسه شهدای ادب',
        verbose_name='نام مدرسه'
    )
    slogan = models.CharField(
        max_length=250,
        blank=True,
        verbose_name='شعار مدرسه'
    )
    address = models.TextField(blank=True, verbose_name='نشانی')
    phone = models.CharField(max_length=30, blank=True, verbose_name='تلفن')
    email = models.EmailField(blank=True, verbose_name='ایمیل')
    academic_year = models.CharField(
        max_length=9,
        blank=True,
        verbose_name='سال تحصیلی'
    )
    about = models.TextField(blank=True, verbose_name='درباره مدرسه')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'تنظیمات مدرسه'
        verbose_name_plural = 'تنظیمات مدرسه'
