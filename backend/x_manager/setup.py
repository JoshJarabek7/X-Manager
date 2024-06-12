"""Module containing the Main X Manager containing the active driver and state"""

import logging
import os
import time
from dotenv import load_dotenv
from .driver import DriverManager
from .cookies import CookieManager
from .account import Account
from .profile import Profile

LOGGER = logging.Logger("__name__")

load_dotenv()


class SetupManager:
    """Manages setup

    Returns:
        Self: SetupManager
    """

    def setup(self):
        """Ensures that the user is logged in and/or has valid cookies to authenticate itself"""
        cookie_manager = CookieManager()
        driver = DriverManager().driver
        account = Account()

        if os.path.exists(cookie_manager.path):
            cookie_manager.load()
            driver.refresh()
            account.login()

        else:
            profile = Profile()
            time.sleep(2)
            if f"https://x.com/{profile.username}" not in driver.current_url:
                account.login()

    def quit(self):
        """Stops the driver from running"""
        driver = DriverManager().driver
        driver.quit()
