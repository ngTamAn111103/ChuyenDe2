from django.db import models
from django.contrib.auth.models import User
from profiles.models import Profile
from posts.models import Post
from datetime import datetime
from django.utils import timezone


class Notification(models.Model):
    # Các loại thông báo
    
    LIKE = 'like'
    COMMENT = 'comment'
    
    NOTIFICATION_TYPES = (
        (LIKE, 'Like'),
        (COMMENT, 'Comment'), 

    )
    # Từ người nào gửi tới
    from_user = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True )
    # Người nhận thông báo
    to_user = models.ForeignKey(Profile, related_name='notifications', on_delete=models.CASCADE)
    # Loại thông báo
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)

    # Của bài viết nào
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # Trạng thái đã đọc/chưa đọc của thông báo.
    is_read = models.BooleanField(default=False)
    # Thời gian tạo thông báo.
    created_at = models.DateTimeField(auto_now_add=True)
    # Thêm các trường khác nếu cần, ví dụ: từ người dùng, bài viết, v.v.

    class Meta:
        ordering = ('-created_at',)
        # 
    def count_unread_notifications(to_user):
        return Notification.objects.filter(is_read=False,to_user=to_user).count()

    def __str__(self):
        return f"vừa {self.notification_type} bài viết của bạn"
    # Lấy thời gian thông báo
    def get_time_elapsed(noti):
        current_time = datetime.now(timezone.utc)
        post_created_time = noti.created_at
        time_difference = current_time - post_created_time

        if time_difference.days > 0:
            if time_difference.days == 1:
                time_elapsed_string = f"{time_difference.days} ngày trước"
            else:
                time_elapsed_string = f"{time_difference.days} ngày trước"
        elif time_difference.seconds > 3600:
            time_difference_hours = time_difference.seconds // 3600
            if time_difference_hours == 1:
                time_elapsed_string = f"{time_difference_hours} giờ trước"
            else:
                time_elapsed_string = f"{time_difference_hours} giờ trước"
        elif time_difference.seconds > 60:
            time_difference_minutes = time_difference.seconds // 60
            if time_difference_minutes == 1:
                time_elapsed_string = f"{time_difference_minutes} phút trước"
            else:
                time_elapsed_string = f"{time_difference_minutes} phút trước"
        else:
            time_elapsed_string = f"{time_difference.seconds} giây trước"

        return time_elapsed_string

