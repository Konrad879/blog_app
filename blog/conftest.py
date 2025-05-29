import pytest
from django.contrib.auth.models import User
from .models import BlogPost, Profile


@pytest.fixture(autouse=True)
def enable_db(transactional_db):
    pass

# Tests of Blog Post Model

@pytest.fixture
def user():
    user = User.objects.create_user(username="testuser", password="password")
    return user

@pytest.fixture
def another_user():
    user = User.objects.create_user(username="liker", password="password")
    user.profile.profile_bio = "test bio"
    user.profile.facebook_link = "https://facebook.com/test"
    user.profile.save()
    return user

@pytest.fixture
def blog_post(user):
    return BlogPost.objects.create(user=user, body="Hello world")

@pytest.fixture
def liked_blog_post(blog_post, another_user):
    blog_post.likes.add(another_user)
    blog_post.save()
    return blog_post

# Tests of Blog Post Model

@pytest.fixture
def profile(user):
    return Profile.objects.get(user=user)

@pytest.fixture
def another_profile(another_user):
    return Profile.objects.get(user=another_user)

@pytest.fixture
def profile_follows():
    pass