import os
import pytest
import json
from playwright.sync_api import Page, expect

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

@pytest.fixture(scope="session")
def test_data():
    # read the file once for a whole session
    with open("posts/tests/test_data/test_data.json", "r", encoding="utf-8") as file:
        return json.load(file)

@pytest.fixture
def authenticated_page(page: Page, live_server, django_user_model, test_data):
    test_username = test_data["user"]["username"]
    test_password = test_data["user"]["password"]

    # test user and database setup

    django_user_model.objects.create_user(
        username=test_username,
        password=test_password
    )

    page.goto(f"{live_server}/login/")

    page.fill("#username-field", test_username)
    page.fill("#password-field", test_password)

    page.click("button[type='submit']")

    assert page.is_visible("text=Logout")
    yield page

@pytest.fixture(autouse=True)
def isolate_media_root(settings, tmpdir):
    # force django to use temporary folder in order to prevent duplicates appearing in the media folder
    settings.MEDIA_ROOT = tmpdir.strpath

@pytest.fixture
def published_post(test_data, authenticated_page):
    # a prepared post to be tested - in order not to repeat the code
    page = authenticated_page
    test_blog_post_text = test_data["post"]["text"]
    page.fill("#id_body", test_blog_post_text)
    page.click("button[type='submit']")
    expect(page.locator(".alert-dark").first).to_contain_text(test_blog_post_text)

    yield page