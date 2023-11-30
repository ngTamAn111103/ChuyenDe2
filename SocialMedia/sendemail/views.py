from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
import random
from django.http import HttpResponse

from django.contrib.auth.models import User
from profiles.models import Profile
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect

    
# Create your views here.
# Hàm xử lý gửi mã OTP vào mail:
def send_OTP(request):
    # Mặc đinh số âm
    otp = -1
    # cờ để báo hiệu đã gửi otp
    flag_send_otp = -1
    # text 
    text = ''
    # Xử lý
    if request.method == 'POST':
        # Lấy email người dùng điền vào form:
        email = request.POST.get('email')
        # Lấy username người dùng điền vào form:
        username = request.POST.get('username')


        # vì email và usernae là duy nhất
        # tìm profile có email và usernae là người dùng điền vào
        profile = Profile.objects.filter(email=email).first()
        # nếu profile có tồn tại
        if profile:
            # tìm tiếp coi username điền có đúng ko
            if profile.username.username == username:
                # Xác thực hợp lệ 
                otp = random.randint(100000, 999999)  # Tạo mã OTP ngẫu nhiên
                message = f'Mã OTP dùng để reset mật khẩu của tài khoản {profile.username}: <strong>{otp}</strong>'
                # Lưu OTP vào session để kiểm tra sau này
                request.session['otp'] = otp
                send_mail(f'Mã OTP để reset mật khẩu cho tài khoản {username}',message,'21211TT3528@mail.tdc.edu.vn',[profile.email], fail_silently=False)
                flag_send_otp = 0
                text = "Đã gửi mã OTP, vui lòng nhập chính xác mã."
            # User name và email không hợp lệ
            else:
                text = 'Username hoặc Email không hợp lệ.'
                flag_send_otp = 1
        else:
            text = 'Tài khoản hoặc email của bạn không tồn tại'
            flag_send_otp = 2
        
       
        
        
    context = {
        'flag_send_otp':flag_send_otp,
        'email' : request.POST.get('email'),
        'username' : request.POST.get('username'),
        'text':text
    }
    return render(request, 'account/forgotpassword.html', context)

def submit_otp(request):
    # Đăng nhập đúng quy trình
    if request.method == 'POST':
        
        # Lấy username người dùng điền vào form:
        username = request.POST.get('username')
        # Lấy username người dùng điền vào form:
        email = request.POST.get('email')
        # Lấy otp người dùng điền vào form:
        otp_user = request.POST.get('otp')
        # nếu OTP có tồn tại
        if otp_user:

            # Lấy otp đã gửi cho người dùng trước đó:
            otp_session = request.session['otp']
        #    Chúng nó khác kiểu dữ liệu
        # So sánh người dùng nhập đúng hay không
            if str(otp_session) == str(otp_user):
                # Xóa toàn bộ ss
                request.session.flush()
                # lưu 1 session để check lại username bên trang reset password
                request.session['username_forgotpassword'] = username
                # Chuyển qua trang reset
                return render(request,'account/resetpassword.html',)
            else:
                context ={
                    'text':'OTP không hợp lệ',
                    'flag_send_otp': 3,
                    'email':email,
                    'username':username,
                }
                return render(request,'account/forgotpassword.html', context)
    # Đăng nhập bằng đường dẫn
    else:
        return redirect('/forgot_password')
def reset_password(request):
    # Đăng nhập đúng quy trình
    if request.method == 'POST':
        print(" if request.method == 'POST':")
        username = request.session.get('username_forgotpassword')
        print(username)
        # Lấy username đang cần QUÊN MẬT KHẨU
        user = User.objects.filter(username=username).first()
        print(user)
        # Nếu tồn tại (không đi đường tắt để lấy mật khẩu)
        if user:
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            print(new_password)
            print(confirm_password)
            # 2 mk giống nhau -> lưu
            if new_password == confirm_password:
                user.set_password(confirm_password)
                user.save()
                # return render(request,'account/resetpassword.html',{'flag' :1})
                return redirect('/')
            # 2 mật khẩu không khớp
            else:
                return render(request,'account/resetpassword.html',{'flag' :-1})

    # Đăng nhập bằng link
    else:
        return redirect('/forgot_password')


    

        
