import pytest
from playwright.sync_api import Page

@pytest.mark.django_db(transaction=True)
def test_user_can_create_a_post(page: Page, live_server, authenticated_page_fixture):
    page = authenticated_page_fixture
    test_blog_post_text = "hi, this is a test blog - text"
    page.fill("#id_body", test_blog_post_text)
    page.click("button[type='submit']")

    assert "hi, this is a test blog - text" in page.content()