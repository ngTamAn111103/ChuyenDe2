from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.shortcuts import render,redirect,get_object_or_404
from .models import Post,Like, Image
from .models import Profile
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required 
from .forms import PostModelForm,CommentModelForm,EditPostModelForm, EditCmtModelForm
from django.http import JsonResponse
from profiles.models import Relationship
from django.views.generic import UpdateView,DeleteView, DetailView
from django.db.models import Q
from .models import Comment
from notification.models import Notification
from chat.models import ChatRoom

# Create your views here.
@login_required()
def post_comment_create_listview(request):
    # lấy tất cả bài viết
    # qs = Post.objects.all()
    
    
    

    # profile của thằng đăng đăng nhập
    profile = Profile.objects.get(username=request.user)
    
    # Bạn bè của profile
    friends = Relationship.objects.filter((Q(sender=profile) | Q(receiver=profile)), status='accepted')
    my_friends=[]
    for friend in friends:
        if friend.sender == profile:
            my_friends.append(friend.receiver)
        else:
            my_friends.append(friend.sender)
    friend_list = Relationship.objects.filter((Q(sender=profile) | Q(receiver=profile)), status='accepted')
    # List rõng
    posts = []

    # Lấy tất cả các bài viết của bạn bè và thêm vào danh sách
    for friend in friends:
        if friend.sender == profile:
            posts += Post.objects.filter(author=friend.receiver).prefetch_related('images')
        else:
            posts += Post.objects.filter(author=friend.sender).prefetch_related('images')

    # Lấy tất cả các bài viết của bạn và thêm vào danh sách
    your_posts = Post.objects.filter(author=profile).prefetch_related('images')

    # Gộp danh sách bài viết của bạn bè và của bạn
    posts += list(your_posts)

    # Sắp xếp danh sách bài viết theo trường "created" (ngày tạo) giảm dần
    posts.sort(key=lambda post: post.created, reverse=True)


    # new post form
    p_form = PostModelForm(request.POST or None, request.FILES or None,request.FILES.getlist('image'))
    # new comment form
    c_form = CommentModelForm(request.POST or None)

    # edit post
    post_edit_id = request.POST.get('post_edit_id')
    post_edit = Post.objects.filter(id=post_edit_id).first()  # Hoặc .get() nếu bạn chắc chắn rằng chỉ có một bài viết phù hợp
    edit_p_form = EditPostModelForm(request.POST or None, request.FILES or None, instance=post_edit)

    # edit cmt
    cmt_edit_id = request.POST.get('edit_cmt_id')
    cmt_edit = Comment.objects.filter(id=cmt_edit_id).first()  # Hoặc .get() nếu bạn chắc chắn rằng chỉ có một bài viết phù hợp
    edit_c_form = EditCmtModelForm(request.POST or None, instance=cmt_edit)

    # Lấy danh sách lời mời kết bạn gửi đến mình
    friend_requests = Relationship.objects.filter((~Q(sender=profile)| ~Q(receiver= profile)), status='send')
    
    
    # Accept request friends
    print("--------------------------------")
    
    
    # Xử lý 
    if request.method == "POST":
        print('if request.method == "POST":')

        

        # delete post 
        post_del_id = request.POST.get('post_del_id')
        if post_del_id:
            print("if post_del_id:")
            # Xóa bài viết
            Post.objects.filter(id=post_del_id).delete()
            return redirect('/')  # Chuyển hướng sau khi gửi thành công
        # delete cmt
        cmt_del_id = request.POST.get('cmt_del_id')
        if cmt_del_id:
            print("if post_del_id:")
            # Xóa bài viết
            Comment.objects.filter(id=cmt_del_id).delete()
            return redirect('/')  # Chuyển hướng sau khi gửi thành công
        # edit post
        elif edit_p_form.is_valid() & (post_edit_id is not None):
            print("elif edit_p_form.is_valid():")

            
            post_edit = edit_p_form.save(commit=False)
            post_edit.author = profile
            post_edit.save()
        # Danh sách img người dùng đăng
            list_img = request.FILES.getlist('image')
            # Có tải hình mới lên
            if len(list_img) >0:
                # Xóa hình cũ
                post_edit.images.all().delete()
                 # Xử lý mỗi file tải lên riêng biệt
                for file in request.FILES.getlist('image'):
                    Image.objects.create(post=post_edit, image=file)
                
               
               
            return redirect('/')  # Chuyển hướng sau khi gửi thành công
        # edit cmt
        elif (edit_c_form.is_valid()) & (cmt_edit_id is not None):
            print('elif edit_c_form.is_valid():')
            author_cmt = Comment.objects.get(id =request.POST.get('edit_cmt_id')).user
            instance = edit_c_form.save(commit=False)
            # instance.user = profile

            instance.user = author_cmt

            instance.save()

            return redirect('/')  # Chuyển hướng sau khi gửi thành công
        # Tạo post
        elif p_form.is_valid():
            print(" elif p_form.is_valid():")
            post = p_form.save(commit=False)
            post.author = profile
            post.save()

            # Xử lý mỗi file tải lên riêng biệt
            for file in request.FILES.getlist('image'):
                Image.objects.create(post=post, image=file)

            return redirect('/')

        # Tạo cmt
        elif c_form.is_valid():
            print('elif c_form.is_valid():')
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentModelForm()
            return redirect('/')
        # Tính năng kết bạn
        elif 'relationship_id' in request.POST and 'btn_relationship' in request.POST:
            print("accept_delete_request(request)")
            accept_delete_request(request) 

        else:
            # pass
            print("không có cái nào vào cả")
    
    # Trả về để test
    notis = Notification.objects.filter(to_user=profile).order_by('is_read')
    # Trả về tát cả chatroom
    chatrooms = ChatRoom.objects.filter(participants=profile)
        # Thêm thông tin về tin nhắn cuối cùng
    for chatroom in chatrooms:
        last_message = chatroom.messages.all().order_by('-timestamp').first()
        chatroom.last_message = last_message if last_message else None


    # Lấy ID của những người dùng trong my_friends
    my_friends_ids = [friend.id for friend in my_friends]

    # Lấy danh sách các user có cùng country và không phải là bạn bè
    FriendSuggesterList = Profile.objects.filter(country=profile.country).exclude(id__in=my_friends_ids + [profile.id])

    # Mảng trả về
    context = {
        'qs': posts,
        'profile': profile,
        'p_form': p_form,
        'c_form': c_form,
        'edit_p_form': edit_p_form,
        'friend_requests': friend_requests,
        'my_notifications': notis,
        'len_my_notifications': (notis.count()),
        'chatrooms': chatrooms,
        'friend_list': my_friends,
        'FriendSuggesterList':FriendSuggesterList,
    }
    print("--------------------------------")
    return render(request, 'main.html', context)

# Like, unlike xử lý ở index
def like_unlike_post(request):
    # Lấy user đăng nhập
    user = request.user
    
    if request.method == 'POST':
        # Lấy trường hidden post_id
        post_id = request.POST.get('post_id')
        print(post_id)
        # tìm bài đăng theo di
        post_obj = Post.objects.get(id=post_id)
        # lấy đối tượng user
        profile = Profile.objects.get(username=user)

        # user nằm trong danh sách đối tượng đã thích
        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)
        
        # Cập nhật lại giá trị value
        # Nếu không có trường 'created'> đã tạo> Đã có dữ liệu trong db
        if not created:
            if like.value =='Like':
                like.value ='Unlike'
            else:
                like.value='Like'
        # Chưa like lần nào: chưa có dữ liệu database
        else:
            like.value='Like'
            
        post_obj.save()
        like.save()

    # Tạo danh sách các người dùng đã like
    likes = post_obj.liked.all()
    likes_data = []
    for profile in likes:
        likes_data.append({
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'avatar_url': profile.avatar.url
        })
        data = {
            'value': like.value,
            'likes': post_obj.liked.all().count(),
            'liked_users': likes_data
        }
        
        return JsonResponse(data, safe=False)


    return redirect('/')
    # return HttpResponse("Like thành công")

# Hàm này để đồng ý hoặc từ chối kết bạn ở trang detail
def accept_delete_request(request):

    relationship_id=request.POST.get('relationship_id')
    relationship = Relationship.objects.get(id=relationship_id)
        # button
    if request.POST.get('btn_relationship') =='Accept':
        relationship.status = 'accepted'
        relationship.save()
    elif request.POST.get('btn_relationship') =='Delete':
        relationship.delete()


# Hàm này để viết bình luận bài viết
def commented(request):
   if request.method == 'POST':
    content = request.POST.get('body')
    post_cmt = Post.objects.get(id=request.POST.get('post_id'))
    user = Profile.objects.get(username = request.user)
    Comment.objects.create(user=user, body= content, post=post_cmt)
    data = {
            'user_name_commented': f'{user.first_name} {user.last_name}',
            'body': content

        }
    return JsonResponse(data, safe=False)
       
# Chi tiết bài viết -> khi nhấn vào 1 noti 
class DetailPost(DetailView):
    model = Post
    template_name = 'detail_post.html'
    def get_object(self):
        post_id =self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        return  post
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object()
        return (context)
    