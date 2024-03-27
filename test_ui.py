from time import sleep

import requests
from selene import browser, have

from allure_commons._allure import step

LOGIN = "example1200@example.com"
PASSWORD = "123456"
WEB_URL = "https://demowebshop.tricentis.com/"
API_URL = "https://demowebshop.tricentis.com/"


def test_login():
    """Successful authorization to some demowebshop (UI)"""
    with step("Open login page"):
        browser.open("http://demowebshop.tricentis.com/login")

    with step("Fill login form"):
        browser.element("#Email").send_keys(LOGIN)
        browser.element("#Password").send_keys(PASSWORD).press_enter()

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))


def test_login_api():
    """Successful authorization to some demowebshop (API)"""
    with step("Authorize user in browser"):
        response = requests.post(url=API_URL + "login", data={"Email": LOGIN, "Password": PASSWORD}, allow_redirects=False)
        cookie = response.cookies.get("NOPCOMMERCE.AUTH")
        browser.open("http://demowebshop.tricentis.com")
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})

    with step("Open main page"):
        browser.open("http://demowebshop.tricentis.com")

    with step("Verify successful authorization"):
        # sleep(5)
        browser.element(".account").should(have.text(LOGIN))


def test_add_to_cart():
    with step("Get user cookie"):
        response = requests.post(url=API_URL + "login", data={"Email": LOGIN, "Password": PASSWORD}, allow_redirects=False)
        cookie = response.cookies.get("NOPCOMMERCE.AUTH")

    with step("Add product to user's cart"):
        add_to_cart_url = "https://demowebshop.tricentis.com/addproducttocart/catalog/31/1/1"
        requests.post(add_to_cart_url, cookies={"NOPCOMMERCE.AUTH": cookie})

    with step("Open cart page"):
        browser.open("http://demowebshop.tricentis.com")
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open("https://demowebshop.tricentis.com/cart")
        sleep(5)
    with step("Check items in cart"):
        pass
        # проверка количества товара в корзине
