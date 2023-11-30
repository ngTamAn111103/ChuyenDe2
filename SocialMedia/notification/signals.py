from django.db.models.signals import post_save
from django.dispatch import receiver
from posts.models import Like, Comment
from profiles.models import Profile, Relationship
from .models import Notification

@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created and instance.user != instance.post.author:
        print("LIKE")
        Notification.objects.create(
            to_user=instance.post.author,
            notification_type=Notification.LIKE,
            from_user = instance.user,
            post=instance.post
        )

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created and instance.user != instance.post.author:
        print("CMT")
        Notification.objects.create(
            from_user = instance.user,
            to_user=instance.post.author,
            notification_type=Notification.COMMENT,
            post=instance.post
        )

