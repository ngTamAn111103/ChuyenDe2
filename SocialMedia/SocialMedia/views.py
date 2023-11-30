from django.http import HttpResponse
from django.shortcuts import render
from profiles.models import Profile
from django.views.generic import CreateView,UpdateView,DetailView,ListView

def home_view(request):
    user = request.user
    profile = None
    if user is not None :
        profile = Profile.objects.get(username=request.user)
    text = "Hello "
    
    context = {
        'user': user,
        'text': text,
        'profile': profile,
    }
    # return render(request, 'main/navbar.html',context)
    return HttpResponse('Hello '+ user.username)


