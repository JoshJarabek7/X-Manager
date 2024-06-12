"""Module containing the Navigator class for navigation between URL paths."""

from .driver import DriverManager
from .profile import Profile


class Navigator:
    """Handles navigation for the web driver."""

    def __init__(self):
        self._driver = DriverManager().driver
        self._profile = Profile()
        self._base_url = "https://x.com"

    def profile(self):
        """Navigates to the user's profile home"""
        url = f"{self._base_url}/{self._profile.username}"
        self._driver.get(url)

    def likes(self):
        """Navigates to the user's likes section"""
        url = f"{self._base_url}/{self._profile.username}/likes"
        self._driver.get(url)

    def replies(self):
        """Navigates to the user's replies section"""
        url = f"{self._base_url}/{self._profile.username}/with_replies"
        self._driver.get(url)
