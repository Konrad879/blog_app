import pytest
from playwright.sync_api import expect


@pytest.mark.django_db(transaction=True)
def test_user_can_create_post_with_text(authenticated_page, test_data):
    # receives a logged user from a fixture
    page = authenticated_page
    # finds a first post in the specified div
    posts = page.locator(".alert-dark")
    # creates a test post with text imported from test_data.json
    test_blog_post_text = test_data["post"]["text"]
    page.fill("#id_body", test_blog_post_text)
    page.click("button[type='submit']")

    expect(posts.first).to_contain_text(test_blog_post_text)


@pytest.mark.django_db(transaction=True)
def test_user_can_create_post_with_text_and_image(authenticated_page, test_data):
    
    page = authenticated_page
    # text and image path imported from 
    
    test_blog_post_text = test_data["post"]["text"]
    page.set_input_files("input[type='file']", test_data["post"]["image_path"])
    page.fill("#id_body", test_blog_post_text)
    
    first_post = page.locator(".alert-dark").first
    page.click("button[type='submit']")

    expect(first_post.get_by_role("img", name="Post image")).to_be_visible()
    expect(first_post).to_contain_text(test_blog_post_text)
    expect(first_post).to_contain_text("@test_user")

   
@pytest.mark.django_db(transaction=True)
def test_user_can_like_a_post(published_post):
    page = published_post
    first_post = page.locator(".alert-dark").first
    first_post.locator(".fa.fa-heart-o").click()

    expect(first_post.locator("#likes")).to_have_text("1")