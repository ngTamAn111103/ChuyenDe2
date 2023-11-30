from django.db import models
# Xử lý đuôi hình ảnh
from django.core.validators import FileExtensionValidator
# Xử lý user like bài
from profiles.models import Profile
from django.utils import timezone
from datetime import datetime
import os

# Create your models here.

class Post (models.Model):
    content = models.TextField(blank=False,default='')
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes')
    commented = models.ManyToManyField(Profile, blank=True, related_name='comments')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='posts')
    STATUS_CHOICES = (
    # Chưa nhấn -> hiển thị thích
    ("Public", "Công khai"),
    # Đã nhấn -> chuyển sang ko thích nữa
    ("Friend", "Bạn bè"),
)
    visibility = models.CharField(max_length=20, choices=(STATUS_CHOICES), default='Public', blank=False)
    def __str__(self) -> str:
        return str(self.content[:50])
    
    
    def num_likes(self):
        return self.liked.all().count()
        # return self.liked.filter().all().count()
        
    def get_image_extension(self):
        if self.image:
            return os.path.splitext(self.image.name)[1]
        return None
    def get_comments(self):
        return self.commented.all()
    def get_likes(self):
        return self.liked.all()
    def num_comments (self):
        return self.comment_set.all().count()
    
    # Lấy số lượng ảnh của bài viết
    def num_images_post(self):
        return self.images.all().count()
    # lấy thời gian đăng bài
    def get_time_elapsed(post):
        current_time = datetime.now(timezone.utc)
        post_created_time = post.created
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




    class Meta:
        ordering = ('-created',)
        
class Comment (models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def get_time_comment(post):
        current_time = datetime.now(timezone.utc)
        post_created_time = post.created
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

    def __str__(self) -> str:
        return str(str(self.user) +" - "+str( self.post.content) +' - '+ str(self.body))
    class Meta:
        ordering = ('-created',)
        
    
LIKE_CHOICES = (
    # Chưa nhấn -> hiển thị thích
    ("Like", "Like"),
    # Đã nhấn -> chuyển sang ko thích nữa
    ("Unlike", "Unlike"),
)
class Like (models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.user}-{self.post}-{self.value}"
    

class Image(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.FileField(upload_to='post', blank=True, 
                             validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'mp4', 'mov'])])
    def __str__(self) -> str:
        return f"{self.image}"
    def get_image_extension(self):
        if self.image:
            return os.path.splitext(self.image.name)[1]