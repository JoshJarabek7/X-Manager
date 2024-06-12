"""Module contains CookieManager class which handles the saving and loading of cookies."""

import json
import logging
from .driver import DriverManager

LOGGER = logging.Logger("__name__")


class CookieManager:
    """Manages Cookies for the web driver.

    Returns:
        Self: CookieManager Instance.
    """

    _cookies_file: str = "cookies.json"

    def save(self):
        """Saves the cookies from the current session to the cookies.json file."""
        with open(self._cookies_file, "w", encoding="utf-8") as f:
            driver = DriverManager().driver
            json.dump(driver.get_cookies(), f)

    def load(self):
        """Loads the cookies from the cookies.json file into the current session."""
        try:
            with open(self._cookies_file, "r", encoding="utf-8") as f:
                cookies = json.load(f)
                driver = DriverManager().driver
                for cookie in cookies:
                    driver.add_cookie(cookie)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            LOGGER.exception(msg=f"Could not load cookies: {e}")

    @property
    def path(self):
        """Gets the path for the cookies.json file

        Returns:
            str: String path of the cookies.json file
        """
        return self._cookies_file
