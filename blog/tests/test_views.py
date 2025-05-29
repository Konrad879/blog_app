import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import BlogPost

@pytest.mark.django_db(transaction=True)
class TestHomeView:

    def test_home_view_as_anonymous_user(self, client):
        url = reverse('home')
        response = client.get(url)
        assert response.status_code == 200
        assert 'blog_posts' in response.context
        assert 'form' not in response.context

    def test_home_view_as_authenticated_user_get(self, client):
        user = User.objects.create_user(username="testuser", password="secret123")
        client.login(username="testuser", password="secret123")

        url = reverse('home')
        response = client.get(url)

        assert response.status_code == 200
        assert 'blog_posts' in response.context
        assert 'form' in response.context

    def test_home_view_post_valid_form(self, client):
        user = User.objects.create_user(username="testuser", password="secret123")
        client.login(username="testuser", password="secret123")

        url = reverse('home')
        data = {
            "body": "This is a test blog post"
        }
        response = client.post(url, data)

        assert response.status_code == 302  # redirect after successful post
        assert BlogPost.objects.count() == 1

        blog_post = BlogPost.objects.first()
        assert blog_post.body == "This is a test blog post"
        assert blog_post.user == user

    def test_home_view_post_invalid_form(self, client):
        user = User.objects.create_user(username="testuser", password="secret123")
        client.login(username="testuser", password="secret123")

        url = reverse('home')
        data = {
            "body": ""
        }
        response = client.post(url, data)

        assert response.status_code == 200
        assert 'form' in response.context
        assert BlogPost.objects.count() == 0