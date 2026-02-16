from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, BlogPost

# Register your models here.


# Unregister Groups
admin.site.unregister(Group)


# Mix profile into User info
class ProfileInline(admin.StackedInline):
    model = Profile

# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    # Just display username fields on admin page
    fields = ["username"]
    inlines = [ProfileInline]


# Unregister initial User
admin.site.unregister(User)

# Register Blog Posts
admin.site.register(BlogPost)


# Reregister User and Profile
admin.site.register(User, UserAdmin)
#admin.site.register(Profile)

