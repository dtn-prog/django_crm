from django.db.models.signals import post_save
from .models import *
from django.contrib.auth.models import User, Group
from django.dispatch import receiver

@receiver(post_save, sender=User)
def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        Customer.objects.create(
            user=instance,
            name=instance.username
        )