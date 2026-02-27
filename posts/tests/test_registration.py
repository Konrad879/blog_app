import pytest
from playwright.sync_api import expect, Page

@pytest.mark.django_db
def test_user_can_register(page: Page, live_server, test_data):
    page.goto(live_server.url)
    page.click("#register")
    page.fill("#id_username", test_data["new_user"]["username"])
    page.fill("#id_first_name", test_data["new_user"]["first_name"])
    page.fill("#id_last_name", test_data["new_user"]["last_name"])
    page.fill("#id_email", test_data["new_user"]["email_address"])
    page.fill("#id_password1", test_data["new_user"]["password"])
    page.fill("#id_password2", test_data["new_user"]["password"])
    
    page.click("button[type='submit']")
    
    welcome_message = page.locator(".alert.alert-light").first

    expect(page).to_have_url(live_server.url + "/")
    expect(welcome_message).to_have_text("You have successfully registered, welcome!")
    expect(page.locator("#logout")).to_have_text("Logout")