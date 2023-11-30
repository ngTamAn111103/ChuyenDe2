from django.urls import path, include
from chat import views as chat_views
from django.contrib.auth.views import LoginView, LogoutView



urlpatterns = [
     path("<slug:slug>", chat_views.chatPage, name="chat-page"),




     path('blocked/', chat_views.block_chatroom, name='block_chatroom'),
     path('newgroupchat/', chat_views.new_groupchat, name='new_groupchat'),
     path('update_groupchat/', chat_views.update_groupchat, name='update_groupchat'),
     path('delete_groupchat/', chat_views.delete_groupchat, name='delete_groupchat'),


]
