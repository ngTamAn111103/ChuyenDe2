from django.db.models.signals import post_save
from django.dispatch import receiver
from profiles.models import Profile, Relationship
from .models import ChatRoom

# @receiver(post_save, sender=Relationship)
# def create_chatroom_when_add_friend(sender, instance, created, **kwargs):
#     if created:
#         chatroom = ChatRoom(name=f"{instance.sender.first_name} {instance.sender.last_name} và {instance.receiver.first_name} {instance.receiver.last_name}")
#         chatroom.save()
#         chatroom.participants.add(instance.sender, instance.receiver)

#         print('created chatroom')


