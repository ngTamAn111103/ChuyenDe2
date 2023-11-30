# pass user http://127.0.0.1:8000/admin/auth/user/add/
from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
from datetime import datetime
from django.utils import timezone
from django.db.models import Q


# Create your models here.
class ProfileManager(models.Manager):
    # Lấy tất cả profiles mình đã gửi lời mời kết bạn:
    def get_all_profiles_to_invite(self, me):
        # Lấy tất cả các profiles (hồ sơ người dùng) trừ profile của người đang thực hiện hàm
        profiles = Profile.objects.all().exclude(username=me)

        # Lấy thông tin của profile của người đang thực hiện hàm
        profile = Profile.objects.get(username=me)

        # Lấy tất cả các mối quan hệ liên quan đến profile của người đang thực hiện hàm
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))

        # Tạo một danh sách chứa các profiles đã chấp nhận mời kết bạn
        accepted = []

        # Duyệt qua tất cả các mối quan hệ
        for rel in qs:
            # Nếu mối quan hệ có trạng thái là 'accepted' (đã chấp nhận)
            if rel.status == "accepted":
                # Thêm người nhận và người gửi của mối quan hệ vào danh sách
                accepted.append(rel.receiver)
                accepted.append(rel.sender)

        # Tìm các profiles có sẵn để mời kết bạn, bằng cách loại bỏ những người đã chấp nhận mời
        available = [profile for profile in profiles if profile not in accepted]

        return available

    def get_all_profiles(self, me):
        # Lấy tất cả danh sách hồ sơ <=> loại trừ mình
        profiles = Profile.objects.all().exclude(username=me)
        return profiles


class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(
        unique=True,
        blank=False,
    )
    bio = models.TextField(default="Chưa có tiểu sử...", max_length=100)
    CHOICE_COUNTRY = (
        ("Đà Nẵng", "Đà Nẵng"),
        ("Hà Nội", "Hà Nội"),
        ("Hải Phòng", "Hải Phòng"),
        ("Hồ Chí Minh", "Hồ Chí Minh"),
        ("An Giang", "An Giang"),
        ("Bà Rịa-Vũng Tàu", "Bà Rịa-Vũng Tàu"),
        ("Bạc Liêu", "Bạc Liêu"),
        ("Bắc Giang", "Bắc Giang"),
        ("Bắc Kạn", "Bắc Kạn"),
        ("Bắc Ninh", "Bắc Ninh"),
        ("Bến Tre", "Bến Tre"),
        ("Bình Định", "Bình Định"),
        ("Bình Dương", "Bình Dương"),
        ("Bình Phước", "Bình Phước"),
        ("Bình Thuận", "Bình Thuận"),
        ("Cà Mau", "Cà Mau"),
        ("Cao Bằng", "Cao Bằng"),
        ("Đắk Lắk", "Đắk Lắk"),
        ("Đắk Nông", "Đắk Nông"),
        ("Điện Biên", "Điện Biên"),
        ("Đồng Nai", "Đồng Nai"),
        ("Đồng Tháp", "Đồng Tháp"),
        ("Gia Lai", "Gia Lai"),
        ("Hà Giang", "Hà Giang"),
        ("Hà Nam", "Hà Nam"),
        ("Hà Tĩnh", "Hà Tĩnh"),
        ("Hải Dương", "Hải Dương"),
        ("Hậu Giang", "Hậu Giang"),
        ("Hòa Bình", "Hòa Bình"),
        ("Hưng Yên", "Hưng Yên"),
        ("Khánh Hòa", "Khánh Hòa"),
        ("Kiên Giang", "Kiên Giang"),
        ("Kon Tum", "Kon Tum"),
        ("Lai Châu", "Lai Châu"),
        ("Lâm Đồng", "Lâm Đồng"),
        ("Lạng Sơn", "Lạng Sơn"),
        ("Lào Cai", "Lào Cai"),
        ("Long An", "Long An"),
        ("Nam Định", "Nam Định"),
        ("Nghệ An", "Nghệ An"),
        ("Ninh Bình", "Ninh Bình"),
        ("Ninh Thuận", "Ninh Thuận"),
        ("Phú Thọ", "Phú Thọ"),
        ("Quảng Bình", "Quảng Bình"),
        ("Quảng Nam", "Quảng Nam"),
        ("Quảng Ngãi", "Quảng Ngãi"),
        ("Quảng Ninh", "Quảng Ninh"),
        ("Quảng Trị", "Quảng Trị"),
        ("Sóc Trăng", "Sóc Trăng"),
        ("Sơn La", "Sơn La"),
        ("Tây Ninh", "Tây Ninh"),
        ("Thái Bình", "Thái Bình"),
        ("Thái Nguyên", "Thái Nguyên"),
        ("Thanh Hóa", "Thanh Hóa"),
        ("Thừa Thiên Huế", "Thừa Thiên Huế"),
        ("Tiền Giang", "Tiền Giang"),
        ("Trà Vinh", "Trà Vinh"),
        ("Tuyên Quang", "Tuyên Quang"),
        ("Vĩnh Long", "Vĩnh Long"),
        ("Vĩnh Phúc", "Vĩnh Phúc"),
    )
    country = models.CharField(max_length=50, blank=False, choices=CHOICE_COUNTRY)
    avatar = models.ImageField(default="avatar_default.jpg", upload_to="avatars/")
    cover = models.ImageField(blank=True, upload_to="covers/")
    friends = models.ManyToManyField(User, blank=True, related_name="friens")
    slug = models.SlugField(
        blank=True,
    )

    CHOICE_GENDER = (
        ("male", "Nam"),
        ("female", "Nữ"),
        ("other", "Khác"),
    )
    gender = models.CharField(choices=CHOICE_GENDER, max_length=6, default="other")
    birthday = models.DateField(blank=True, default="2000-01-01")
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ProfileManager()
    # Lấy danh sách bạn bè
    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

    # Lấy số lượng bạn bè
    def get_count_friends(self):
        return (self.friends.all()).count()

    # Lấy số lượng bài đăng
    def get_count_posts(self):
        return self.posts.all().count()

    def get_all_authors_posts(self):
        return self.posts.all()

    # đếm số lượng lượt thích mà người dùng đã thực hiện.
    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_liked = 0
        for i in likes:
            if i.value == "Like":
                total_liked += 1
        return total_liked

    # số lượng lượt thích đã nhận
    def get_likes_recieved_no(self):
        posts = self.posts.all()
        total_liked = 0
        for i in posts:
            total_liked += i.liked.all().count()
        return total_liked

    # Trả về trong admin thông tin
    def __str__(self) -> str:
        return f"{self.id} / {self.username}"

    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name

    # Hàm lưu
    def save(self, *args, **kwargs):
        # Slug cho profile
        self.slug_default()

        # Update hình ảnh default
        self.update_avatar_default()
        super().save(*args, **kwargs)

    # Hàm tạo slug cho profile
    def slug_default(self):
        ex = False
        to_slug = self.slug
        # Nếu có họ và tên
        if (
            self.first_name != self.__initial_first_name
            or self.last_name != self.__initial_last_name
            or self.slug == ""
        ):
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
                ex = Profile.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    ex = Profile.objects.filter(slug=to_slug).exists()
            # Nếu không có họ và tên
            else:
                to_slug = str(self.username)
        self.slug = to_slug

    # Khi người dùng thay đổi giới tính && avatar đang ở mặc định
    # Avatar sẽ thay đổi theo
    def update_avatar_default(self):
        if self.gender == "female" and self.avatar.name == "avatar_default.jpg":
            self.avatar = "avatar_default_nu.jpg"
            self.save()

        if self.gender == "male" and self.avatar.name == "avatar_default_nu.jpg":
            self.avatar = "avatar_default.jpg"
            self.save()


class RelationshipManager(models.Manager):
    def invatations_received(self, receier):
        # Lấy ra những lời mời kết bạn có người nhận == receier
        qs = Relationship.objects.filter(receiver=receier, status="send")
        return qs


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="receiver"
    )
    STATUS_CHOICES = (
        ("send", "Gửi"),
        ("accepted", "Chấp nhận"),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)

    objects = RelationshipManager()

    def __str__(self) -> str:
        return f"{self.sender} - {self.receiver} - {self.status}"
        # lấy thời gian gửi lời mời

    def get_time_elapsed(Relationship):
        current_time = datetime.now(timezone.utc)
        post_created_time = Relationship.created
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
