from django.db import models
from django.contrib.auth.models import User
from profiles.models import Profile
from django.template.defaultfilters import slugify
import unidecode
import random
import uuid


# Đại diện cho 1 phòng chat
# 1-1: participants chỉ chứa 2 người
class ChatRoom(models.Model):
    name = models.CharField(max_length=1000)
    # Những người tham gia phòng chat
    participants = models.ManyToManyField(Profile, related_name="chatrooms")
    # Nếu là chat 1-1: lấy avt đối phương
    # Nếu chat 1-n: lấy avt nhóm
    avatar_room = models.ImageField(default="avatar_default.jpg", upload_to="avatars/")
    slug = models.SlugField(blank=False, default="123123", unique=True)
    group_chat = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}/{self.name}'

    # Hàm lưu
    def save(self, *args, **kwargs):
        if not self.id:  # Kiểm tra nếu đối tượng chưa có ID (tức là mới tạo)
            # Tạo slug ngẫu nhiên
            self.slug = uuid.uuid4().hex[:6].lower()
            while ChatRoom.objects.filter(slug=self.slug).exists():
                self.slug = uuid.uuid4().hex[:6].lower()

        super().save(*args, **kwargs)

        


class BlockChat(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    profile_block = models.ForeignKey(
        Profile, on_delete=models.CASCADE, name="profile_block"
    )

    def __str__(self):
        return f"{self.profile_block.username} đã block chatroom {self.chatroom}"


# Quản lý thông tin thành viên trong mỗi ChatRoom
# Đối với chat 1-1, sẽ có hai Membership cho mỗi Profile.
# Đối với chat nhóm, có thể có nhiều Membership tương ứng với số lượng thành viên trong nhóm.
class Membership(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["chatroom", "profile"]

    def __str__(self):
        return f"{self.profile.username.username} in {self.chatroom.id}"


# Message: Lưu trữ tin nhắn được gửi trong mỗi ChatRoom.
# Mô hình này phục vụ cho cả chat 1-1 và nhóm,
# với sender là người gửi và chatroom là phòng chat mà tin nhắn được gửi đến.
class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    chatroom = models.ForeignKey(
        ChatRoom, related_name="messages", on_delete=models.CASCADE
    )
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} in ChatRoom {self.chatroom.id}: {self.text}"


class Image(models.Model):
    message = models.ForeignKey(
        Message, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="chat_images/")

    def __str__(self):
        return f"Image in Message {self.message.id}"
