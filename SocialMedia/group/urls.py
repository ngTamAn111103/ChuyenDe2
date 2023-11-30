from django.urls import path, re_path
from . import views




app_name = 'group'

urlpatterns =[
    path('search/', views.search, name='search'),
    path('detail_group/<slug:slug>/', views.detail_group, name='detail_group'),
    path('my_list_group/', views.my_list_group, name='my_list_group'),
    path('list_members_group/<slug:slug>', views.list_members_group, name='list_members_group'),
    path('view_group_join_requests/<slug:slug>', views.view_group_join_requests, name='view_group_join_requests'),


    
    path('new_post_group/', views.new_post_group, name='new_post_group'),
    path('edit_post_group/', views.edit_post_group, name='edit_post_group'),
    path('del_post_group/', views.del_post_group, name='del_post_group'),


    path('like_unlike_post/', views.like_unlike_post, name='like_unlike_post'),

    # duyệt yêu cầu vào gr
    path('accepted_join_requests/', views.accepted_join_requests, name='accepted_join_requests'),
    # xóa yêu cầu vào gr
    path('delete_join_requests/', views.delete_join_requests, name='delete_join_requests'),
    # yêu cầu join vào group
    path('request_joingroup/<id>', views.request_joingroup, name='request_joingroup'),
    # rời gr
    path('leave_group/', views.leave_group, name='leave_group'),
    # update gr
    path('update_group/', views.update_group, name='update_group'),
    # giải tán gr
    path('dissolve_group/', views.dissolve_group, name='dissolve_group'),
    # tạo gr
    path('create_group/', views.create_group, name='create_group'),
    # cmt post gr
    path('cmt_post_group/', views.cmt_post_group, name='cmt_post_group'),
    # edit cmt post gr
    path('edit_cmt_group/', views.edit_cmt_group, name='edit_cmt_group'),
    # xóa cmt gr
    path('del_cmt_post_group/', views.del_cmt_post_group, name='del_cmt_post_group'),
    


    path('group/<slug:slug>/', views.detail_group, name='group_detail'),  # Đây là URL pattern cho 'group_detail'

]