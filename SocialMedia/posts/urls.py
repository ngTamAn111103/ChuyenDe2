from django.urls import path, re_path
from .views import post_comment_create_listview, like_unlike_post,commented
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.models import User
from posts.views import DetailPost




app_name = 'posts'

urlpatterns =[
    # index
    path('', views.post_comment_create_listview, name='main_post_view'),
    # chi tiết bài viết (khi nhấn vào 1 noti -> qua đây)
    path('detail_post/<post_id>/', DetailPost.as_view(), name='detail_post'),


    # Like unlike ở index
    path('liked/', views.like_unlike_post, name='like_post_view'),
    # cmt ở index
    path('commented/', views.commented, name='commented'),

]