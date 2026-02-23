import pytest
from playwright.sync_api import Page, expect


@pytest.mark.django_db(transaction=True)
def test_user_can_create_post_with_text(live_server, authenticated_page_fixture, test_data_fixture):
    # receives a logged user from a fixture
    page = authenticated_page_fixture
    # finds a first post in the specified div
    posts = page.locator(".alert-dark")
    # creates a test post with text imported from test_data.json
    test_blog_post_text = test_data_fixture["post"]["text"]
    page.fill("#id_body", test_blog_post_text)
    page.click("button[type='submit']")

    expect(posts.first).to_contain_text(test_blog_post_text)


@pytest.mark.django_db(transaction=True)
def test_user_can_create_post_with_text_and_image(live_server, authenticated_page_fixture, test_data_fixture):
    
    page = authenticated_page_fixture
    posts = page.locator(".alert-dark")
    test_blog_post_text = test_data_fixture["post"]["text"]
    page.set_input_files("input[type='file']", test_data_fixture["post"]["image_path"])
    page.fill("#id_body", test_blog_post_text)
    page.click("button[type='submit']")
    first_post = page.locator(".alert-dark").first

    expect(first_post.get_by_role("img", name="Post image")).to_be_visible()
    expect(first_post).to_contain_text(test_blog_post_text)
    expect(first_post).to_contain_text("@test_user")
    