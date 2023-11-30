from django import forms
from .models import Profile, User,Relationship
from django.contrib.auth.forms import UserCreationForm

# Có dùng để sửa đổi profile trong main.html
class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name','last_name','bio','country','avatar','cover','gender','birthday')
        
# Đăng nhập
class LoginModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password')
        

# Đăng ký
class SignUpModelForm(forms.ModelForm):
    first_name = forms.CharField(label='Họ')
    last_name = forms.CharField(label='Tên')
    username = forms.CharField(label='Tài khoản')
    email = forms.CharField(label='Mail')
    password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Nhập lại mật khẩu', widget=forms.PasswordInput())
    # Chọn thành phố 
    CHOICE_COUNTRY = (
        ('Hồ Chí Minh', 'Hồ Chí Minh'),
    ('Đà Nẵng', 'Đà Nẵng'),
    ('Hà Nội', 'Hà Nội'),
    ('Hải Phòng', 'Hải Phòng'),
    
    ('An Giang', 'An Giang'),
    ('Bà Rịa-Vũng Tàu', 'Bà Rịa-Vũng Tàu'),
    ('Bạc Liêu', 'Bạc Liêu'),
    ('Bắc Giang', 'Bắc Giang'),
    ('Bắc Kạn', 'Bắc Kạn'),
    ('Bắc Ninh', 'Bắc Ninh'),
    ('Bến Tre', 'Bến Tre'),
    ('Bình Định', 'Bình Định'),
    ('Bình Dương', 'Bình Dương'),
    ('Bình Phước', 'Bình Phước'),
    ('Bình Thuận', 'Bình Thuận'),
    ('Cà Mau', 'Cà Mau'),
    ('Cao Bằng', 'Cao Bằng'),
    ('Đắk Lắk', 'Đắk Lắk'),
    ('Đắk Nông', 'Đắk Nông'),
    ('Điện Biên', 'Điện Biên'),
    ('Đồng Nai', 'Đồng Nai'),
    ('Đồng Tháp', 'Đồng Tháp'),
    ('Gia Lai', 'Gia Lai'),
    ('Hà Giang', 'Hà Giang'),
    ('Hà Nam', 'Hà Nam'),
    ('Hà Tĩnh', 'Hà Tĩnh'),
    ('Hải Dương', 'Hải Dương'),
    ('Hậu Giang', 'Hậu Giang'),
    ('Hòa Bình', 'Hòa Bình'),
    ('Hưng Yên', 'Hưng Yên'),
    ('Khánh Hòa', 'Khánh Hòa'),
    ('Kiên Giang', 'Kiên Giang'),
    ('Kon Tum', 'Kon Tum'),
    ('Lai Châu', 'Lai Châu'),
    ('Lâm Đồng', 'Lâm Đồng'),
    ('Lạng Sơn', 'Lạng Sơn'),
    ('Lào Cai', 'Lào Cai'),
    ('Long An', 'Long An'),
    ('Nam Định', 'Nam Định'),
    ('Nghệ An', 'Nghệ An'),
    ('Ninh Bình', 'Ninh Bình'),
    ('Ninh Thuận', 'Ninh Thuận'),
    ('Phú Thọ', 'Phú Thọ'),
    ('Quảng Bình', 'Quảng Bình'),
    ('Quảng Nam', 'Quảng Nam'),
    ('Quảng Ngãi', 'Quảng Ngãi'),
    ('Quảng Ninh', 'Quảng Ninh'),
    ('Quảng Trị', 'Quảng Trị'),
    ('Sóc Trăng', 'Sóc Trăng'),
    ('Sơn La', 'Sơn La'),
    ('Tây Ninh', 'Tây Ninh'),
    ('Thái Bình', 'Thái Bình'),
    ('Thái Nguyên', 'Thái Nguyên'),
    ('Thanh Hóa', 'Thanh Hóa'),
    ('Thừa Thiên Huế', 'Thừa Thiên Huế'),
    ('Tiền Giang', 'Tiền Giang'),
    ('Trà Vinh', 'Trà Vinh'),
    ('Tuyên Quang', 'Tuyên Quang'),
    ('Vĩnh Long', 'Vĩnh Long'),
    ('Vĩnh Phúc', 'Vĩnh Phúc'),
    )

    
# Sắp xếp mảng CHOICE_COUNTRY theo value từ A đến Z
    CHOICE_COUNTRY = sorted(CHOICE_COUNTRY, key=lambda x: x[1])
    country = forms.ChoiceField(choices= CHOICE_COUNTRY, label="Thành phố",initial='Hồ Chí Minh')
    
    CHOICE_GENDER = (
    ('male', 'Nam'),
    ('female', 'Nữ'),
    ('other', 'Khác'),
)
    gender = forms.ChoiceField(choices= CHOICE_GENDER, label="Giới tính")
    # birthday = forms.CharField(max_length=10, label="Ngày sinh",widget=forms.TextInput(placeholder="DD/MM/YYYY"))
    birthday = forms.CharField(max_length=10, label="Ngày sinh", 
                               widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    
   



    class Meta:
        model = User
        fields = ('first_name','last_name', 'username','email', 'password1', 'password2', 'country','gender','birthday')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Profile.objects.filter(email=email).exists():
            raise forms.ValidationError("Email đã tồn tại.")
        return email
    # Cấu hình bắt lỗi
    def clean_username(self):
        # Kiểm tra xem tài khoản đã tồn tại chưa
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Tài khoản đã tồn tại. Vui lòng chọn một tài khoản khác.")
        return username
    def clean_password2(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Mật khẩu xác nhận không khớp.")
# Lâm: Đổi mk: resetpaswordmodelform
#  3 trường: pass cũ, pas mới 1, pass mới 2
# đăng ký các trường cho người dùng nhập

# Trường để người dùng nhập dữ liệu
class ChangePasswordModelForm(forms.ModelForm):
    password_old = forms.CharField(label='Mật khẩu cũ',widget=forms.PasswordInput)
    password1 = forms.CharField(label='Mật khẩu mới',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Xác nhận mật khẩu',widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('password_old','password1', 'password2')
    
    def clean_password2(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Mật khẩu xác nhận không khớp.")
        return cleaned_data
class RelationshipModelForm(forms.ModelForm):
    class Meta:
        model = Relationship
        fields = ('status',) 
   


    
