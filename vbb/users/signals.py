from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import User


@receiver(post_save, sender=User)
def send_mentor_registration_notification(sender, instance, created, **kwargs):
    # Check if a new user was created and if they are a mentor
    if created and instance.is_mentor:
        # Send an email notification to the admin
        send_mail(
            subject="New Mentor Registration",
            message=f"A new mentor has registered: {instance.first_name} {instance.last_name} (Email: {instance.email})",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )
