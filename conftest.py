import os
import pytest
import json
from playwright.sync_api import Page

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

@pytest.fixture(scope="session")
def test_data_fixture():
    # read the file once for a whole session
    with open("posts/tests/test_data.json", "r", encoding="utf-8") as file:
        return json.load(file)

@pytest.fixture
def authenticated_page_fixture(page: Page, live_server, django_user_model, test_data_fixture):
    test_username = test_data_fixture["user"]["username"]
    test_password = test_data_fixture["user"]["password"]

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