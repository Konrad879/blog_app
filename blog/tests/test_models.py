import pytest
from django.utils import timezone


@pytest.mark.django_db(transaction=True)
class TestBlogPostModel:
    
    def test_number_of_likes_zero(self, blog_post):
        assert blog_post.number_of_likes() == 0

    def test_number_of_likes_one(self, liked_blog_post):
        assert liked_blog_post.number_of_likes() == 1
    
    def test_str_representation(self, blog_post, monkeypatch):
        fixed_time = timezone.now().replace(year=2020, month=1, day=1, hour=12, minute=0, second=0)
        monkeypatch.setattr(blog_post, 'created_at', fixed_time)
        expected = f"{blog_post.user} ({fixed_time: %Y-%m-%d %H:%M}) {blog_post.body}..."
        assert str(blog_post) == expected


@pytest.mark.django_db(transaction=True)
class TestProfileModel:

    def test_str_representation(self, profile):
        assert str(profile) == profile.user.username

    def test_profile_has_bio_if_none(self, profile):
        assert profile.profile_bio == None

    def test_profile_has_bio_not_none(self, another_profile):
        assert another_profile.profile_bio == "test bio"

    def test_profile_links_if_none(self, profile):
        assert profile.homepage_link == None
        assert profile.facebook_link == None
        assert profile.instagram_link == None
        assert profile.linkedin_link == None

    def test_profile_links_if_not_none(self, another_profile):
        assert another_profile.facebook_link == "https://facebook.com/test"