
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        return super().create_superuser(
            username, email, password, **extra_fields
        )


class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = 'admin', 'مدیر'
        TEACHER = 'teacher', 'دبیر'
        STUDENT = 'student', 'دانش‌آموز'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.STUDENT,
        verbose_name='نقش کاربر'
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        verbose_name='شماره تماس'
    )

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.get_full_name() or self.username} - {self.get_role_display()}'
