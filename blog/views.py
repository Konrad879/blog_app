from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, BlogPost

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        blog_posts = BlogPost.objects.all().order_by("-created_at")

    return render(request, 'home.html', {"blog_posts":blog_posts})

def profile_list(request):

    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {'profiles': profiles})
    else:
        messages.success(request, ("You must be logged in to view this page..."))
        return redirect('home')
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        blog_posts = BlogPost.objects.filter(user_id=pk).order_by("-created_at")
        
        # Post Form Logic
        if request.method=="POST":
            # Get current user
            current_user_profile = request.user.profile
            # Get form data
            action = request.POST['follow']
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            # Save the profile
            current_user_profile.save()
            

        return render(request, "profile.html", {"profile":profile, "blog_posts":blog_posts})
    else:
        messages.success(request, ("You must be logged in to view this page..."))
        return redirect('home')
    

