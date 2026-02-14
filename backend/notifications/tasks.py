"""
Celery tasks for notifications
"""
from celery import shared_task
from datetime import datetime, timedelta
from django.utils import timezone
from notifications.models import Notification
from scholarships.models import Scholarship, Application
from profiles.models import Profile


@shared_task
def check_deadlines():
    """
    Check for scholarships with deadlines within 7 days and send notifications
    """
    seven_days_from_now = timezone.now().date() + timedelta(days=7)
    today = timezone.now().date()
    
    # Find scholarships with deadlines in the next 7 days
    upcoming_scholarships = Scholarship.objects.filter(
        is_approved=True,
        is_active=True,
        deadline__gte=today,
        deadline__lte=seven_days_from_now
    )
    
    notifications_created = 0
    
    for scholarship in upcoming_scholarships:
        # Find users who have bookmarked or applied to this scholarship
        from scholarships.models import Bookmark
        
        bookmarked_users = Bookmark.objects.filter(scholarship=scholarship).values_list('user', flat=True)
        applied_users = Application.objects.filter(scholarship=scholarship).values_list('user', flat=True)
        
        all_users = set(list(bookmarked_users) + list(applied_users))
        
        for user in all_users:
            # Check if notification already exists
            if not Notification.objects.filter(
                user=user,
                scholarship_id=scholarship.id,
                notification_type='deadline_approaching',
                is_read=False
            ).exists():
                days_left = (scholarship.deadline - today).days
                Notification.objects.create(
                    user=user,
                    notification_type='deadline_approaching',
                    title=f'Deadline Approaching: {scholarship.title}',
                    message=f'The deadline for {scholarship.title} is in {days_left} day(s). Don\'t miss out!',
                    link=f'/scholarships/{scholarship.id}',
                    scholarship_id=scholarship.id
                )
                notifications_created += 1
    
    return f"Created {notifications_created} deadline notifications"


@shared_task
def check_incomplete_profiles():
    """
    Check for users with incomplete profiles and send notifications
    """
    from accounts.models import User
    from notifications.signals import check_profile_completeness
    
    students = User.objects.filter(role='student')
    notifications_created = 0
    
    for user in students:
        check_profile_completeness(user)
        notifications_created += 1
    
    return f"Checked {notifications_created} user profiles"

