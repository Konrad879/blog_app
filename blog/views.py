from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, BlogPost
from .forms import BlogPostForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        form = BlogPostForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                blog_post = form.save(commit=False)
                blog_post.user = request.user
                blog_post.save()
                messages.success(request, ("Your blog post has been posted..."))
                return redirect('home')

        blog_posts = BlogPost.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"blog_posts":blog_posts, "form":form})
    else:
        blog_posts = BlogPost.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"blog_posts":blog_posts})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {'profiles': profiles})
    else:
        messages.success(request, ("You must be logged in to view this page..."))
        return redirect('home')
    

def unfollow(request, pk):
	if request.user.is_authenticated:
		# Get the profile to unfollow
		profile = Profile.objects.get(user_id=pk)
		# Unfollow the user
		request.user.profile.follows.remove(profile)
		# Save our profile
		request.user.profile.save()

		# Return message
		messages.success(request, (f"You Have Successfully Unfollowed {profile.user.username}"))
		return redirect(request.META.get("HTTP_REFERER"))

	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
		return redirect('home')

def follow(request, pk):
	if request.user.is_authenticated:
		# Get the profile to unfollow
		profile = Profile.objects.get(user_id=pk)
		# Unfollow the user
		request.user.profile.follows.add(profile)
		# Save our profile
		request.user.profile.save()

		# Return message
		messages.success(request, (f"You Have Successfully Followed {profile.user.username}"))
		return redirect(request.META.get("HTTP_REFERER"))

	else:
		messages.success(request, ("You Must Be Logged In To View This Page..."))
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
    
def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:        
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'followers.html', {'profiles': profiles})
        else:
            messages.success(request, ("That's not your profile page..."))
            return redirect('home')     
    else:
        messages.success(request, ("You must be logged in to view this page..."))
        return redirect('home')
    

def follows(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:        
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'follows.html', {'profiles': profiles})
        else:
            messages.success(request, ("That's not your profile page..."))
            return redirect('home')     
    else:
        messages.success(request, ("You must be logged in to view this page..."))
        return redirect('home')
          

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
         
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been successfully logged in!"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error logging in. Please try again"))
            return redirect('login')


    else:
        return render(request, "login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been successfully logged out!"))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']
        
            # Log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have successfully registered, welcome!"))
            return redirect('home')

    return render(request, "register.html", {'form':form})


def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		profile_user = Profile.objects.get(user__id=request.user.id)
		# Get Forms
		user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
		profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()

			login(request, current_user)
			messages.success(request, ("Your Profile Has Been Updated!"))
			return redirect('home')

		return render(request, "update_user.html", {'user_form':user_form, 'profile_form':profile_form})
	else:
		messages.success(request, ("You Must Be Logged In To View That Page..."))
		return redirect('home')
        

def blog_post_like(request, pk):
    if request.user.is_authenticated: 
        blog_post = get_object_or_404(BlogPost, id=pk)
        if blog_post.likes.filter(id=request.user.id):
            blog_post.likes.remove(request.user)
        else:
             blog_post.likes.add(request.user)
        # Redirect to the last visited site
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, ("You Must Be Logged In To View That Page..."))
        return redirect('home')

def blog_post_share(request, pk):
    blog_post = get_object_or_404(BlogPost, id=pk)
    if blog_post:
        return render(request, "blog_post_share.html", {'blog_post':blog_post})

    else:
        messages.success(request, ("That Blog Post does not exist"))
        return redirect('home')