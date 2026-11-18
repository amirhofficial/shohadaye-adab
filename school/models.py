
from django.conf import settings
from django.db import models


class FieldOfStudy(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='نام رشته'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'رشته تحصیلی'
        verbose_name_plural = 'رشته‌های تحصیلی'


class Grade(models.Model):
    LEVEL_CHOICES = [
        (10, 'دهم'),
        (11, 'یازدهم'),
        (12, 'دوازدهم'),
    ]

    level = models.PositiveSmallIntegerField(
        choices=LEVEL_CHOICES,
        unique=True,
        verbose_name='پایه'
    )

    def __str__(self):
        return self.get_level_display()

    class Meta:
        verbose_name = 'پایه تحصیلی'
        verbose_name_plural = 'پایه‌های تحصیلی'
        ordering = ['level']


class Classroom(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='نام کلاس'
    )

    grade = models.ForeignKey(
        Grade,
        on_delete=models.PROTECT,
        related_name='classrooms',
        verbose_name='پایه'
    )

    field = models.ForeignKey(
        FieldOfStudy,
        on_delete=models.PROTECT,
        related_name='classrooms',
        verbose_name='رشته'
    )

    academic_year = models.CharField(
        max_length=9,
        verbose_name='سال تحصیلی'
    )

    def __str__(self):
        return f'{self.grade} {self.field} - {self.name}'

    class Meta:
        verbose_name = 'کلاس'
        verbose_name_plural = 'کلاس‌ها'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'grade', 'field', 'academic_year'],
                name='unique_class_per_year'
            )
        ]


class Subject(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='نام درس'
    )

    field = models.ForeignKey(
        FieldOfStudy,
        on_delete=models.PROTECT,
        related_name='subjects',
        verbose_name='رشته'
    )

    grade = models.ForeignKey(
        Grade,
        on_delete=models.PROTECT,
        related_name='subjects',
        verbose_name='پایه'
    )

    def __str__(self):
        return f'{self.name} - {self.grade} {self.field}'

    class Meta:
        verbose_name = 'درس'
        verbose_name_plural = 'درس‌ها'


class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.PROTECT,
        related_name='students',
        null=True,
        blank=True,
        verbose_name='کلاس'
    )

    student_number = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True,
        verbose_name='شماره دانش‌آموزی'
    )

    def __str__(self):
        return f'{self.user.get_full_name()} - {self.classroom}'

    class Meta:
        verbose_name = 'پرونده دانش‌آموز'
        verbose_name_plural = 'پرونده‌های دانش‌آموزان'


class TeacherProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )

    subjects = models.ManyToManyField(
        Subject,
        related_name='teachers',
        blank=True,
        verbose_name='دروس تدریسی'
    )

    classrooms = models.ManyToManyField(
        Classroom,
        related_name='teachers',
        blank=True,
        verbose_name='کلاس‌های تدریس'
    )

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    class Meta:
        verbose_name = 'پرونده دبیر'
        verbose_name_plural = 'پرونده‌های دبیران'



class Assignment(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان تکلیف')
    description = models.TextField(verbose_name='توضیحات')
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name='کلاس'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name='assignments',
        verbose_name='درس'
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='created_assignments',
        verbose_name='دبیر'
    )
    due_date = models.DateTimeField(verbose_name='مهلت انجام')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'تکلیف'
        verbose_name_plural = 'تکالیف'
        ordering = ['due_date']


class WeeklySchedule(models.Model):
    class WeekDay(models.IntegerChoices):
        SATURDAY = 0, 'شنبه'
        SUNDAY = 1, 'یکشنبه'
        MONDAY = 2, 'دوشنبه'
        TUESDAY = 3, 'سه‌شنبه'
        WEDNESDAY = 4, 'چهارشنبه'
        THURSDAY = 5, 'پنجشنبه'
        FRIDAY = 6, 'جمعه'

    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name='کلاس'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        verbose_name='درس'
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name='دبیر'
    )
    weekday = models.IntegerField(
        choices=WeekDay.choices,
        verbose_name='روز هفته'
    )
    start_time = models.TimeField(verbose_name='ساعت شروع')
    end_time = models.TimeField(verbose_name='ساعت پایان')

    def __str__(self):
        return f'{self.classroom} - {self.subject}'

    class Meta:
        verbose_name = 'برنامه هفتگی'
        verbose_name_plural = 'برنامه هفتگی'
        ordering = ['weekday', 'start_time']


class SchoolAnnouncement(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    content = models.TextField(verbose_name='متن اطلاعیه')
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        related_name='announcements',
        null=True,
        blank=True,
        verbose_name='کلاس مقصد'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='school_announcements',
        verbose_name='نویسنده'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True, verbose_name='منتشر شود')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'اطلاعیه'
        verbose_name_plural = 'اطلاعیه‌ها'
        ordering = ['-created_at']


class GradeRecord(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='grades',
        verbose_name='دانش‌آموز'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        verbose_name='درس'
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='recorded_grades',
        verbose_name='دبیر'
    )
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='نمره'
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='توضیحات'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student} - {self.subject}: {self.score}'

    class Meta:
        verbose_name = 'نمره'
        verbose_name_plural = 'نمرات'
        ordering = ['-created_at']
