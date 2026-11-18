

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from school.models import StudentProfile, TeacherProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

    if instance.role == User.Role.STUDENT:
        StudentProfile.objects.get_or_create(user=instance)

    elif instance.role == User.Role.TEACHER:
        TeacherProfile.objects.get_or_create(user=instance)
