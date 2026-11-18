
from django.contrib import admin
from .models import (
    FieldOfStudy,
    Grade,
    Classroom,
    Subject,
    StudentProfile,
    TeacherProfile,
)


@admin.register(FieldOfStudy)
class FieldOfStudyAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('level',)


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'field', 'academic_year')
    list_filter = ('grade', 'field', 'academic_year')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'field')
    list_filter = ('grade', 'field')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_number', 'classroom')
    list_filter = ('classroom',)


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('subjects', 'classrooms')
