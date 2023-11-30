from django.shortcuts import render
from django.http import HttpResponse
from .models import Group, GroupMembership, Post, Comment, Like
from profiles.models import Profile
from django.db.models import Q
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
import json
from django.http import JsonResponse
from django.db.models import Value
from django.db.models.functions import Concat
from posts.models import Post as post_main



def search(request):
    q = request.GET.get('key', '')  # Lấy từ khóa từ request
    # Sử dụng __icontains để tìm kiếm gần đúng
    list_group = Group.objects.filter(name__icontains=q)

    # Tạo trường full_name bằng cách ghép first_name và last_name
    list_user = Profile.objects.annotate(
        full_name=Concat('first_name', Value(' '), 'last_name')
    ).filter(
        # Tìm kiếm trong trường full_name
        Q(full_name__icontains=q)
    )
    context = {
        'list_group': list_group,
        'list_user': list_user,

    }
    return render(request, 'list_search.html', context)


def detail_group(request,slug):
    profile = Profile.objects.get(username=request.user)

    # Thông tin của nhóm
    group = Group.objects.get(slug=slug)

    # Lấy các bài post của nhóm
    posts = Post.objects.filter(group=group)
    # Lấy bình luận cho mỗi bài post
    for post in posts:
        post.comments = Comment.objects.filter(post=post)

    # Lấy thông tin joined_at từ GroupMembership
    try:
        membership = GroupMembership.objects.get(group=group, user=profile.username)
        joined_at = membership.joined_at
    except GroupMembership.DoesNotExist:
        joined_at = ''  # Hoặc bạn có thể đặt một giá trị mặc định
    # Kiểm tra xem có là thành viên của gr chưa
    is_member = GroupMembership.objects.filter(user=request.user, group=group, is_approved=True).exists()
    # kiểm tra xem đã gửi lời mời chưa
    join_request_sent = GroupMembership.objects.filter(user=profile.username, group=group, is_approved=False).exists()

   
    context = {
        'group':group,
        'posts':posts,
        'profile':profile,
        'joined_at': joined_at,  # Thêm thông tin này vào context
        'is_member':is_member,
        'join_request_sent':join_request_sent
        
    }
    return render(request,'group.html',context)

def my_list_group(request):
    # Lấy ra tất cả các GroupMembership nơi user hiện tại là thành viên và đã được phê duyệt
    group_memberships = GroupMembership.objects.filter(user=request.user, is_approved=True)

    # Lấy ra tất cả các nhóm từ các GroupMembership tìm được
    groups_joined = [membership.group for membership in group_memberships]


        # Lấy ra tất cả các nhóm mà người dùng chưa tham gia
    # Điều này bao gồm những nhóm mà người dùng không phải là thành viên hoặc chưa được phê duyệt
    groups_not_joined = Group.objects.exclude(id__in=[group.id for group in groups_joined])


    # Gửi các nhóm này tới template
    context = {
        'groups_joined': groups_joined,
        'groups_not_joined':groups_not_joined,
    }
    return render(request, 'my_list_group.html', context)

# Tạo bài viết mới
def new_post_group(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        group = Group.objects.get(id=group_id)
        author = Profile.objects.get(username=request.user)
        content = request.POST.get('content')
        image = request.FILES.get('image') if 'image' in request.FILES else None
        Post.objects.create(group=group, content=content, image=image,author=author)
        return redirect(f'/group/detail_group/{group.slug}')
    return redirect(f'/group/detail_group/{group.slug}')

def edit_post_group(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        group = Group.objects.get(id=group_id)

        post_edit_id = request.POST.get('post_id')
        post_edit = Post.objects.get(id=post_edit_id)

        post_edit.content = request.POST.get('content')
        if request.FILES.get('image'):
            post_edit.image = request.FILES.get('image')

        post_edit.save()
        return redirect(f'/group/detail_group/{group.slug}')
    return redirect(f'/group/detail_group/{group.slug}')

def del_post_group(request):

    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        group = Group.objects.get(id=group_id)

        post_del_id = request.POST.get('post_del_id')
        post_del = Post.objects.get(id=post_del_id)
        post_del.delete()
        
        return redirect(f'/group/detail_group/{group.slug}')
    return redirect(f'/group/detail_group/{group.slug}')


def like_unlike_post(request):
    # Lấy user đăng nhập
    user = request.user
    group_id = request.POST.get('group_id')
    group = Group.objects.get(id=group_id)
    if request.method == 'POST':
        # Lấy trường hidden post_id
        post_id = request.POST.get('post_id')
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
    return redirect(f'/group/detail_group/{group.slug}')


def list_members_group(request, slug):
    profile = Profile.objects.get(username=request.user)

    group = get_object_or_404(Group, slug=slug)

    # Lấy ra danh sách các admin của nhóm
    admin_memberships = GroupMembership.objects.filter(group=group, user__in=group.admins.all())

    # Tạo một danh sách chứa thông tin của các admin bao gồm profile và ngày tham gia
    admins_info = [{
        'profile': admin.user.profile,
        'joined_at': admin.joined_at
    } for admin in admin_memberships if hasattr(admin.user, 'profile')]
    # Lấy ra danh sách bạn bè của người dùng
    friends = profile.get_friends()

    # Lấy ra tất cả thành viên của nhóm
    group_memberships = GroupMembership.objects.filter(group=group)

        # Lọc ra những bạn bè cũng là thành viên của nhóm
    friends_in_group = [{
        'profile': membership.user.profile,
        'joined_at': membership.joined_at
    } for membership in group_memberships if membership.user in friends]

        # Lấy thông tin profile và joined_at của tất cả thành viên
    all_members_info = [{
        'profile': membership.user.profile,
        'joined_at': membership.joined_at
    } for membership in group_memberships if hasattr(membership.user, 'profile')]


    context = {
        'admins_info': admins_info,
        'friends_in_group': friends_in_group,
        'all_members_info': all_members_info,


    }
    return render(request, 'members_group.html', context)

# Lấy danh sách người dùng xin tham gia vào nhóm
def view_group_join_requests(request, slug):
    # Lấy thông tin profile của người dùng hiện tại
    profile = Profile.objects.get(username=request.user)

    # Lấy thông tin nhóm dựa trên slug
    group = get_object_or_404(Group, slug=slug)

    # Kiểm tra xem người dùng hiện tại có phải là admin của nhóm không
    if request.user in group.admins.all():
        # Lấy ra các yêu cầu xin vào nhóm chưa được phê duyệt
        join_requests = GroupMembership.objects.filter(group=group, is_approved=False)

        # Lấy ra profile của mỗi người dùng trong danh sách yêu cầu
        requested_profiles = [membership.user.profile for membership in join_requests if hasattr(membership.user, 'profile')]

        context = {
            'group': group, 
            'join_requests': requested_profiles,
        }

        # Trả về HttpResponse hoặc render tới một template với danh sách các profile
        return render(request, 'list_user_join_group.html', context)
    else:
        # Nếu người dùng không phải là admin, trả về một HttpResponse hoặc redirect
        return HttpResponse("Bạn không có quyền xem yêu cầu tham gia nhóm này.")


# Hàm duyệt yêu cầu vào nhóm đơn
def accepted_join_requests(request):
    group = get_object_or_404(Group, id=request.POST.get('group_id'))
    if request.method == 'POST':
        profile_id= request.POST.get('profile_id')

        profile=Profile.objects.get(id=profile_id)

        request_joingroup = GroupMembership.objects.get(user=profile.username)
        request_joingroup.is_approved = True
        request_joingroup.save()
    
            # print("\033[91m{}\033[0m".format(profile_ids_json))
    return redirect(f'/group/view_group_join_requests/{group.slug}')





# Hàm xóa yêu cầu vào nhóm đơn
def delete_join_requests(request):
    group = get_object_or_404(Group, id=request.POST.get('group_id'))
    if request.method == 'POST':
        profile_id= request.POST.get('profile_id')
        profile=Profile.objects.get(id=profile_id)
        print(profile)
        request_joingroup = GroupMembership.objects.get(user=profile.username)
        request_joingroup.delete()
    
    return redirect(f'/group/view_group_join_requests/{group.slug}')


            
# Yêu cầu vào gr
def request_joingroup(request,id):
    if request.method == 'POST':
        # group = Group.objects.get(id = request.POST.get('group_id'))
        group = Group.objects.get(id = id)
        GroupMembership.objects.create(group=group, user=request.user)
    
        return redirect(f'/group/detail_group/{group.slug}')
# Rời gr
def leave_group(request):
    if request.method == 'POST':
        # Lấy gr
        group = Group.objects.get(id = request.POST.get('group_id'))
        # lấy user
        user = request.user
        # Trường hợp tao là admin và 
        if user in group.admins.all():
            # chỉ còn 1 admin: tao rời nhóm > giải tán nhóm
            if group.admins.all().count() == 1:
                group.delete()
                return redirect(f'/group/my_list_group/')
            # còn nhiều admin
            else:
                group.admins.remove(user)
                GroupMembership.objects.get(group=group, user=user, is_approved=True).delete()
        # Không phải admin
        else:
            GroupMembership.objects.get(group=group, user=user, is_approved=True).delete()

    
        return redirect(f'/group/detail_group/{group.slug}')
    
def update_group(request):
    group = Group.objects.get(id=request.POST.get('group_id'))
    if request.method == 'POST':
        group.name = request.POST.get('name')
        group.description = request.POST.get('description')
        group.visibility = request.POST.get('visibility')  # Cập nhật visibility từ form

        if request.FILES.get('avatar'):
            group.avatar = request.FILES.get('avatar')
        if request.FILES.get('cover'):
            group.cover = request.FILES.get('cover')
        group.save() 
    return redirect(f'/group/detail_group/{group.slug}')

def dissolve_group(request):
    group = Group.objects.get(id=request.POST.get('group_id'))
    if request.method == "POST":
        group.delete()
    return redirect('/')

def create_group(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        visibility = request.POST.get('visibility')

        # Tạo đối tượng Group mới
        new_group = Group.objects.create(
            name=name, 
            description=description, 
            visibility=visibility
        )

        # Thêm người dùng hiện tại làm admin của nhóm
        new_group.admins.add(request.user)

        # Tạo một membership cho người dùng hiện tại và đánh dấu là đã được chấp thuận
        GroupMembership.objects.create(
            group=new_group,
            user=request.user,
            is_approved=True
        )

        # Xử lý file ảnh cho avatar và cover nếu có
        if 'avatar' in request.FILES:
            new_group.avatar = request.FILES['avatar']
        if 'cover' in request.FILES:
            new_group.cover = request.FILES['cover']
        new_group.save()

        # Redirect sau khi tạo nhóm
        # return redirect('some_url_after_creation')  # Thay 'some_url_after_creation' bằng URL cần redirect

    # Nếu không phải POST request, redirect người dùng
        return redirect(f'/group/detail_group/{new_group.slug}')
    return redirect('/group/my_list_group/')


def cmt_post_group(request):
    group = Group.objects.get(id=request.POST.get('group_id'))
    if request.method == 'POST':
        post = Post.objects.get(id = request.POST.get('post_id'))
        Comment.objects.create(
            user=Profile.objects.get(username=request.user),
            post=post,
            body=request.POST.get('content_cmt'),
        )
    return redirect(f"/group/detail_group/{group.slug}")

def edit_cmt_group(request):
    group_id = request.POST.get('group_id')
    group = Group.objects.get(id=group_id)
    if request.method == 'POST':
        
        comment_id = request.POST.get('comment_id')
        comment_content = request.POST.get('comment_content')

        # Lấy comment dựa trên ID
        cmt = Comment.objects.get(id=comment_id)  # Đảm bảo rằng bạn đã nhập đúng tên lớp mô hình cho Comment

        # Cập nhật nội dung comment
        cmt.body = comment_content
        cmt.save()  # Sử dụng save() thay vì update()

    return redirect(f"/group/detail_group/{group.slug}")

def del_cmt_post_group(request):
    group_id = request.POST.get('group_id')
    group = Group.objects.get(id=group_id)
    if request.method == 'POST':
        
        comment_id = request.POST.get('comment_id')
        comment_content = request.POST.get('comment_content')

        # Lấy comment dựa trên ID
        cmt = Comment.objects.get(id=comment_id)  # Đảm bảo rằng bạn đã nhập đúng tên lớp mô hình cho Comment

      
        cmt.delete()  # Sử dụng save() thay vì update()

    return redirect(f"/group/detail_group/{group.slug}")
