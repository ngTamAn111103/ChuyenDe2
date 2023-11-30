"""
URL configuration for SocialMedia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view
from profiles import views
from django.urls import re_path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView




urlpatterns = [
    # trang admin
    path('admin/', admin.site.urls),

    # Trang index: Posts
    path('', include('posts.urls'), name='posts'),
    # Vào trong url profile: http://127.0.0.1:8000/profiles/myprofile/
    path('profiles/', include('profiles.urls'), name='profiles'),
    path('forgot_password/', include('sendemail.urls'), name='forgot_password'),
    
    # đăng ký
    path('register', views.SignUp.as_view(), name='signup'),

    # đăng nhập
    path("login", auth_views.LoginView.as_view(template_name="account/login.html"),name='login'),
    # đăng xuất
    path('logout', LogoutView.as_view(), name='logout'),

    # chat 
    path('chat/', include(('chat.urls', 'chat'), namespace='chat')),

    # group
    path('group/', include(('group.urls', 'group'), namespace='group')),






    
    




    
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
