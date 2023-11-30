from django.contrib import admin
from .models import Group,Post,GroupMembership, Like, Comment
# Register your models here.

admin.site.register(Post)
admin.site.register(Group)
admin.site.register(GroupMembership)
admin.site.register(Like)
admin.site.register(Comment)

