from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from profiles.models import Profile
from datetime import datetime
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import os
import uuid
from django.template.defaultfilters import slugify
from profiles.utils import get_random_code



class Group(models.Model):
    name = models.CharField(max_length=100)
    avatar = models.ImageField(default="avatar_default.jpg", upload_to="avatars/",blank=True)
    cover = models.ImageField(default="avatar_default.jpg", upload_to="avatars/", blank=True)
    description = models.TextField(default="Mô tả nhóm....")
    created_at = models.DateTimeField(auto_now_add=True)
    admins = models.ManyToManyField(User, related_name='admins_group')
    STATUS_CHOICES = (("Public", "Công khai"),("Private", "Riêng tư"),)
    visibility = models.CharField(max_length=20, choices=(STATUS_CHOICES), default='Public', blank=False)
    slug = models.SlugField(
        blank=True,
    )
    def get_count_members(self):
        return self.memberships.filter(is_approved=True).count()
    def get_members(self):
        # Lấy ra các đối tượng GroupMembership đã được phê duyệt
        approved_memberships = self.memberships.filter(is_approved=True)

        # Từ các đối tượng GroupMembership, lấy ra các đối tượng User tương ứng
        members = [membership.user for membership in approved_memberships]

        # Lấy ra các Profile tương ứng với mỗi User
        member_profiles = [member.profile for member in members if hasattr(member, 'profile')]

        return member_profiles

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
         # Chỉ tạo slug mới khi đối tượng này chưa có slug
        if not self.slug:
            self.slug_default()


        super().save(*args, **kwargs)

    # Hàm tạo slug cho profile
    def slug_default(self):
        ex = False
        to_slug = self.slug
        # Nếu có họ và tên

            
        to_slug = slugify(f'{self.name}')
        ex = Group.objects.filter(slug=to_slug).exists()
        while ex:
            to_slug = slugify(to_slug + " " + str(get_random_code()))
            ex = Group.objects.filter(slug=to_slug).exists()
           
        self.slug = to_slug


    

class GroupMembership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_memberships')
    # đã vào hay chưa
    is_approved = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('group', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.group.name} // {self.is_approved}"


class Post(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE,related_name='post_groups')
    content = models.TextField(blank=False,default='')
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes_post_group')
    commented = models.ManyToManyField(Profile, blank=True, related_name='comments_post_group')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='author_post_group')
    image = models.ImageField(blank=True, upload_to='post/')

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
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
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
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.user}-{self.post}-{self.value}"
    

