from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, AcademicInfo, CareerPreferences, ProfileCompletion

@receiver(post_save, sender=User)
def create_related(sender, instance, created, **kwargs):
    if created:
        AcademicInfo.objects.create(user=instance)
        CareerPreferences.objects.create(user=instance)
        ProfileCompletion.objects.create(user=instance)
