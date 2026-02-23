import os
import pytest
from datetime import datetime
import json
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

@pytest.fixture
def authenticated_page_fixture(page: Page, live_server, django_user_model):
    test_username = "test_user"
    test_password = "admin123!"

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