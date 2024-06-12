"""Module contains the Account class with manages account related activities."""

import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementNotVisibleException,
    ElementNotInteractableException,
    WebDriverException,
)
from x_manager.profile import Profile
from x_manager.driver import DriverManager

from x_manager.cookies import CookieManager

LOGGER = logging.Logger("__name__")


class Account:
    """Manages the Account related activities, such as authentication.

    Returns:
        Self: Account Instance
    """

    _login_url: str = "https://x.com/login"

    def _input_username(self):
        driver = DriverManager().driver
        profile = Profile()
        try:
            username_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//input[@autocomplete="username"]')
                )
            )
            username_input.send_keys(profile.username)
        except (
            NoSuchElementException,
            TimeoutException,
            ElementNotVisibleException,
            ElementNotInteractableException,
        ) as e:
            LOGGER.exception("Could not input username: %s", e)
        except WebDriverException as e:
            LOGGER.exception("WebDriver error occured while inputting username: %s", e)

    def _input_password(self, return_after=True):
        profile = Profile()
        driver = DriverManager().driver
        try:
            password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//input[@autocomplete="current-password"]')
                )
            )
            password_input.send_keys(profile.password)
            if return_after:
                password_input.send_keys(Keys.ENTER)
        except (
            NoSuchElementException,
            TimeoutException,
            ElementNotVisibleException,
            ElementNotInteractableException,
        ) as e:
            LOGGER.exception("Could not input password: %s", e)
        except WebDriverException as e:
            LOGGER.exception("WebDriver error occurred while inputting password: %s", e)

    def login(self):
        """Log Account into X and save cookies

        TODO: Add 2FA features into management browser

        """
        driver = DriverManager().driver
        driver.get(self._login_url)
        time.sleep(2)
        self._input_password()
        time.sleep(2)
        self._input_password()
        CookieManager().save()
