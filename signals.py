from django.db.models.signals import post_save
from django.dispatch import receiver
from monitor.models import EventLog
from .utils import send_sms_alert  # Function we'll create
import logging

@receiver(post_save, sender=EventLog)
def alert_caregivers(sender, instance, created, **kwargs):
    if created:
        # Check if event requires alert (e.g., 'emotion' with severity 'high')
        if instance.event_type in ['emotion', 'voice', 'movement'] and instance.severity == 'high':
            send_sms_alert(instance.patient)
