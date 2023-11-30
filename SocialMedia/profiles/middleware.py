# profiles/middleware.py

from django.shortcuts import redirect

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path == '/profiles/myprofile/':
            return redirect('login')  # Chuyển hướng đến trang đăng nhập nếu chưa đăng nhập
        response = self.get_response(request)
        return response
