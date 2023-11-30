from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Like, Post
from profiles.models import Profile


@receiver(post_save, sender=Like)
def post_save_like(sender, instance, created, **kwargs):
    user = instance.user
    post = instance.post
    if instance.value == "Like":
        post.liked.add(user)
    elif instance.value == "Unlike":
        post.liked.remove(user)
    post.save()


