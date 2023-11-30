from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.models import User
from sendemail.views import send_OTP,submit_otp




app_name = 'sendemail'

urlpatterns =[
    # Link 
    path('', views.send_OTP, name='main_forgot_password_view'),
    path('submit_otp/', views.submit_otp, name='submit_otp'),
    path('reset_password/', views.reset_password, name='reset_password'),

    

]