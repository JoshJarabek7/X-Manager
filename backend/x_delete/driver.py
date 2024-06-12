"""Module containing the DriverManager class that keeps track of the webdriver"""

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options


class DriverManager:
    """Singleton class that manages the web driver.

    Returns:
        Self: DriverManager Instance
    """

    _driver: webdriver.Firefox

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(DriverManager, cls).__new__(cls)
            cls.instance._driver = webdriver.Firefox(
                service=Service("/usr/local/bin/geckodriver"), options=Options()
            )
        return cls.instance

    @property
    def driver(self) -> webdriver.Firefox:
        """Gets the web driver.

        Returns:
            webdriver.Firefox: The active web driver.
        """
        return self._driver
