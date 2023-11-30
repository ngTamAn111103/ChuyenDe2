from django.urls import path, re_path
from .views import (my_profile_view,
                    invites_received_view, 
                    profiles_list_view, 
                    invite_profiles_list_view, 
                    ProfileListView,
                    send_invation, 
                    remove_from_friends,
                    accept_invite,
                    reject_invite,
                    ProfileDetailView,
                    change_profile,
                    FriendsListView,
                    like_my_post,
                    edit_post_myprofile,
                    message
                    )
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.models import User
from sendemail.views import send_OTP



app_name = 'profiles'

urlpatterns =[
    path('myprofile/', views.my_profile_view, name='my_profile_view'),
    # Trang cá nhân của người khác
    path('<slug>/', ProfileDetailView.as_view(), name='profile_detail_view'),



    # LÂM: Đổi mật khẩu
    path('myprofile/change_password/', views.ChangePassword.as_view(), name='change_password'),
    # hiển thị danh sách các lời mời kết bạn đã nhận được
    path('myprofile/my_invites/', invites_received_view, name='my_invites_view'),
    # hiển thị danh sách các hồ sơ người dùng trừ hồ sơ của người đang đăng nhập.
    path('myprofile/all_profiles/', ProfileListView.as_view(), name='all_profiles_view'),
    # Link này cùng nhau tạo ra trang web hiển thị danh sách các profiles có sẵn để mời kết bạn, loại trừ những người đã có mối quan hệ chấp nhận.
    path('myprofile/to_invite/', invite_profiles_list_view, name='invite_profiles_view'),
    # Thay đổi thông tin cá nhân profile
    path('myprofile/change_profile/', change_profile, name='change_profile'),
    # Danh sách bạn bè theo slug
    path('<slug>/friends', views.FriendsListView.as_view(), name='friends'),

    








    # Link này được thiết kế để xử lý việc gửi lời mời kết bạn tới người khác: Link ẩn để kết nối form xử lý
    path('myprofile/send_invite/', send_invation, name='send_invite'),


    # Link này được thiết kế để xử lý việc xóa bạn bè: Link ẩn để kết nối form xử lý
    path('myprofile/remove_friend/', remove_from_friends, name='remove_friend'),


    # Link này được thiết kế để xử lý việc đồng ý lời mời kết bạn: Link ẩn để kết nối form xử lý
    path('myprofile/my_invites/acctept', accept_invite, name='accept_invite'),


    # Link này được thiết kế để xử lý việc từ chối lời mời kết bạn: Link ẩn để kết nối form xử lý
    path('myprofile/my_invites/reject', reject_invite, name='reject_invite'),
    # Like unlike ở myprofile
    path('liked_my_post', like_my_post, name='liked_my_post'),
    # edit post ở myprofile
    path('edit_post', edit_post_myprofile, name='edit_post'),

    # nhắn tin với người khác
    path('message', message, name='message'),
    

]