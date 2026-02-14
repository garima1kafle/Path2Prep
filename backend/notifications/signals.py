from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from notifications.models import Notification
from scholarships.models import Scholarship, Application
from profiles.models import Profile


@receiver(post_save, sender=Scholarship)
def notify_new_scholarship(sender, instance, created, **kwargs):
    """Notify users when a new scholarship is approved that matches their profile"""
    if created and instance.is_approved:
        # This will be enhanced with actual matching logic
        pass


def check_profile_completeness(user):
    """Check if user profile is complete and notify if not"""
    try:
        profile = Profile.objects.get(user=user)
        incomplete_fields = []
        
        if not profile.gpa:
            incomplete_fields.append('GPA')
        if not profile.degree_level:
            incomplete_fields.append('Degree Level')
        if not profile.major:
            incomplete_fields.append('Major')
        if not profile.country:
            incomplete_fields.append('Country')
        
        if incomplete_fields:
            Notification.objects.create(
                user=user,
                notification_type='profile_incomplete',
                title='Complete Your Profile',
                message=f'Please complete the following fields: {", ".join(incomplete_fields)}',
                link='/profile'
            )
    except Profile.DoesNotExist:
        Notification.objects.create(
            user=user,
            notification_type='profile_incomplete',
            title='Create Your Profile',
            message='Complete your profile to get personalized scholarship recommendations.',
            link='/profile'
        )

