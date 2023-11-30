from django.contrib import admin
from .models import ChatRoom,Image,Membership,Message, BlockChat
# Register your models here.
admin.site.register(ChatRoom)
admin.site.register(BlockChat)
admin.site.register(Image)
admin.site.register(Membership)
admin.site.register(Message)