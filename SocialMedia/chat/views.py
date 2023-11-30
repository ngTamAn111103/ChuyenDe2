

# # Create your views here.
# from django.shortcuts import render, redirect,get_object_or_404
# from profiles.models import Profile
# from .models import ChatRoom,Message,BlockChat, Membership
# from django.http import HttpResponse
# import uuid
# from .forms import EditChatRoomForm

# def chatPage(request, slug, *args, **kwargs):
# 	# nếu chưa đăng nhập -> chuyển đến login
# 	if not request.user.is_authenticated:
# 		return redirect("login")
# 	# Lấy profile
# 	profile = Profile.objects.get(username=request.user)
# 	# Lấy tất cả đoạn chat để để bên trái
# 	my_chatrooms = get_chatroom(request)

# 	# Nội dung đoạn chat ở bên phải
# 	# Lấy đoạn chat dựa trên slug
# 	chatroom = get_object_or_404(ChatRoom, slug=slug)
# 	block_chatroom = BlockChat.objects.filter(chatroom=chatroom).first()
# 	# Lấy tin nhắn của đoạn chat
# 	messages = chatroom.messages.all().order_by('timestamp')

# 	my_friends = profile.get_friends()

# 	# Code cầm cố
# 	last_message = Message.objects.filter()
# 	if profile not in chatroom.participants.all():
# 		return redirect("/")
	
# 	edit_chatroom_from = EditChatRoomForm()


# 	context = {
# 		'profile':profile,
# 		'my_chatrooms':my_chatrooms,
# 		'chatroom': chatroom,
# 		'messages': messages,
# 		'block_chatroom':block_chatroom,
# 		'my_friends':my_friends,
# 		'edit_chatroom_from':edit_chatroom_from


# 	}
# 	return render(request, "chat.html", context)


# # Lấy tất cả chatroom có request.user ở trong đó
# def get_chatroom(request):
# 	user = request.user
# 	profile = Profile.objects.get(username = user)
# 	my_chatrooms = ChatRoom.objects.filter(participants=profile)
# 		# Thêm thông tin về tin nhắn cuối cùng
# 	for chatroom in my_chatrooms:
# 		last_message = chatroom.messages.all().order_by('-timestamp').first()
# 		chatroom.last_message = last_message if last_message else None
# 	return my_chatrooms

# def block_chatroom(request):
# 	profile = Profile.objects.get(username= request.user)
# 	chatroom_block = ChatRoom.objects.get(id= request.POST.get('chatroom_id'))
# 	obj=BlockChat.objects.filter(profile_block = profile, chatroom=chatroom_block)
# 	# Nếu chưa có: Tạo
# 	if obj:
# 		obj.delete()
# 	else:
# 		BlockChat.objects.create(profile_block = profile, chatroom=chatroom_block)


# 	slug = chatroom_block.slug
# 	return redirect(f'/chat/{slug}')



# def new_groupchat(request):
# 	if request.method == 'POST':
# 		# Lấy thông tin từ form
# 		group_name = request.POST.get('groupName')
# 		member_ids = request.POST.getlist('member')  # 'member' là tên của input checkbox
# 		slug = uuid.uuid4()
# 		print(slug)
# 		# Tạo chat room mới
# 		chatroom = ChatRoom.objects.create(
# 			name=group_name,
# 			group_chat=True,  # Đánh dấu đây là chat nhóm
# 			slug = slug,
# 		)
# 		chatroom.save()  # Lưu chatroom để có thể thêm thành viên

# 		# Thêm người dùng hiện tại và các thành viên được chọn vào chatroom
# 		for member_id in member_ids:
# 			profile = Profile.objects.get(id=member_id)
# 			chatroom.participants.add(profile)
		
# 		# Thêm người dùng hiện tại là người tạo nhóm làm admin
# 		user_profile = Profile.objects.get(username=request.user)
# 		chatroom.participants.add(user_profile)  # Đảm bảo người tạo nhóm cũng là thành viên
		
# 		# Tạo membership và đặt người dùng hiện tại là admin
# 		Membership.objects.create(
# 			chatroom=chatroom,
# 			profile=user_profile,
# 			is_admin=True
# 		)
		
# 		# Redirect to the chat room page or somewhere else
# 		return redirect('chat:chat-page', slug=slug)
# 	else:
# 		# Nếu không phải POST request, hiển thị lỗi hoặc redirect
# 		return HttpResponse("Invalid request", status=400)
	
# # def update_groupchat(request):
# # 	if request.method == 'POST':

# # 		chatroom = ChatRoom.objects.get(id=request.POST.get('chatroom_id'))
# # 		slug = chatroom.slug
	
# # 		chatroom.name = request.POST.get('groupName')
# # 		if request.POST.get('groupAvatar'):
# # 			chatroom.avatar_room = request.POST.get('groupAvatar')
			
# # 		chatroom.save()
		
		
# # 		return redirect(f'/chat/{slug}')
# def delete_groupchat(request):

# 	if request.method == 'POST':

# 		chatroom = ChatRoom.objects.get(id=request.POST.get('chatroom_id'))
# 		chatroom.delete()

		
		
# 		return redirect(f'/')

# def update_groupchat(request):
#     if request.method == 'POST':
#         # Sử dụng get_object_or_404 để tránh lỗi khi không tìm thấy ChatRoom
#         chatroom_id = request.POST.get('chatroom_id')
#         chatroom = get_object_or_404(ChatRoom, id=chatroom_id)
#         chatroom.name = request.POST.get('groupName')
#         avatar_file = request.FILES.get('groupAvatar')
#         if avatar_file:chatroom.avatar_room.save(avatar_file.name, avatar_file)


			
		




      

        
#         # Lưu cập nhật thông tin nhóm
#         chatroom.save()

        
#         # Chuyển hướng người dùng đến trang chatroom mới được cập nhật
#         return redirect('chat:chat-page', slug=chatroom.slug)
#     else:
#         return redirect('chat:chat-page', slug=chatroom.slug)


# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from profiles.models import Profile
from .models import ChatRoom, Message, BlockChat, Membership
from django.http import HttpResponse
import uuid



def chatPage(request, slug, *args, **kwargs):
    # nếu chưa đăng nhập -> chuyển đến login
    if not request.user.is_authenticated:
        return redirect("login")
    # Lấy profile
    profile = Profile.objects.get(username=request.user)
    # Lấy tất cả đoạn chat để để bên trái
    my_chatrooms = get_chatroom(request)

    # Nội dung đoạn chat ở bên phải
    # Lấy đoạn chat dựa trên slug
    chatroom = get_object_or_404(ChatRoom, slug=slug)
    block_chatroom = BlockChat.objects.filter(chatroom=chatroom).first()
    # Lấy tin nhắn của đoạn chat
    messages = chatroom.messages.all().order_by("timestamp")

    my_friends = profile.get_friends()

    # Code cầm cố
    last_message = Message.objects.filter()
    if profile not in chatroom.participants.all():
        return redirect("/")

    is_admin = False
    try:
        membership = Membership.objects.get(chatroom=chatroom, profile=request.user.profile)
        is_admin = membership.is_admin
    except Membership.DoesNotExist:
        pass


    context = {
        "profile": profile,
        "my_chatrooms": my_chatrooms,
        "chatroom": chatroom,
        "messages": messages,
        "block_chatroom": block_chatroom,
        "my_friends": my_friends,
        'is_admin':is_admin,

    }
    return render(request, "chat.html", context)


# Lấy tất cả chatroom có request.user ở trong đó
def get_chatroom(request):
    user = request.user
    profile = Profile.objects.get(username=user)
    my_chatrooms = ChatRoom.objects.filter(participants=profile)
    # Thêm thông tin về tin nhắn cuối cùng
    for chatroom in my_chatrooms:
        last_message = chatroom.messages.all().order_by("-timestamp").first()
        chatroom.last_message = last_message if last_message else None
    return my_chatrooms


def block_chatroom(request):
    profile = Profile.objects.get(username=request.user)
    chatroom_block = ChatRoom.objects.get(id=request.POST.get("chatroom_id"))
    obj = BlockChat.objects.filter(profile_block=profile, chatroom=chatroom_block)
    # Nếu chưa có: Tạo
    if obj:
        obj.delete()
    else:
        BlockChat.objects.create(profile_block=profile, chatroom=chatroom_block)

    slug = chatroom_block.slug
    return redirect(f"/chat/{slug}")


def new_groupchat(request):
    if request.method == "POST":
        # Lấy thông tin từ form
        group_name = request.POST.get("groupName")
        member_ids = request.POST.getlist(
            "member"
        )  # 'member' là tên của input checkbox
        # Tạo chat room mới
        chatroom = ChatRoom(
            name=group_name,
            group_chat=True,  # Đánh dấu đây là chat nhóm
        )
        chatroom.save()  # Lưu chatroom để có thể thêm thành viên

        # Thêm người dùng hiện tại và các thành viên được chọn vào chatroom
        for member_id in member_ids:
            profile = Profile.objects.get(id=member_id)
            chatroom.participants.add(profile)

        # Thêm người dùng hiện tại là người tạo nhóm làm admin
        user_profile = Profile.objects.get(username=request.user)
        chatroom.participants.add(
            user_profile
        )  # Đảm bảo người tạo nhóm cũng là thành viên

        # Tạo membership và đặt người dùng hiện tại là admin
        Membership.objects.create(
            chatroom=chatroom, profile=user_profile, is_admin=True
        )
        # Nhưng người dùng khác ko phải admin
        for member_id in member_ids:
            profile = Profile.objects.get(id=member_id)
            Membership.objects.create(
            chatroom=chatroom, profile=profile, is_admin=False
        )


        # Redirect to the chat room page or somewhere else
        return redirect("chat:chat-page", slug=chatroom.slug)
    else:
        # Nếu không phải POST request, hiển thị lỗi hoặc redirect
        return HttpResponse("Invalid request", status=400)


# def update_groupchat(request):
# 	if request.method == 'POST':

# 		chatroom = ChatRoom.objects.get(id=request.POST.get('chatroom_id'))
# 		slug = chatroom.slug

# 		chatroom.name = request.POST.get('groupName')
# 		if request.POST.get('groupAvatar'):
# 			chatroom.avatar_room = request.POST.get('groupAvatar')

# 		chatroom.save()


# 		return redirect(f'/chat/{slug}')
def delete_groupchat(request):

    if request.method == "POST":

        chatroom = ChatRoom.objects.get(id=request.POST.get("chatroom_id"))
        chatroom.delete()

        return redirect(f"/")


def update_groupchat(request):
    if request.method == "POST":
        # Sử dụng get_object_or_404 để tránh lỗi khi không tìm thấy ChatRoom
        chatroom_id = request.POST.get("chatroom_id")
        chatroom = get_object_or_404(ChatRoom, id=chatroom_id)
        chatroom.name = request.POST.get("groupName")
        # avatar_file = request.FILES.get("avatar_room")
        if request.FILES.get("avatar_room"):
            chatroom.avatar_room = request.FILES.get("avatar_room")


        # Lưu cập nhật thông tin nhóm
        chatroom.save()

        # Chuyển hướng người dùng đến trang chatroom mới được cập nhật
        return redirect("chat:chat-page", slug=chatroom.slug)
    else:
        return redirect("chat:chat-page", slug=chatroom.slug)
