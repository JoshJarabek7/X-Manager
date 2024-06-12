"""Module containing the Profile class"""

import os

class Profile:
    """Keeps track of Profile related data, like username and password."""
    _username: str = os.getenv("USERNAME", "")
    _password: str = os.getenv("PASSWORD", "")

    @property
    def username(self):
        """Gets profile's username.

        Returns:
            str: Profile's username.
        """
        return self._username

    @property
    def password(self):
        """Gets profile's password.

        Returns:
            str: Profile's password.
        """
        return self._password
