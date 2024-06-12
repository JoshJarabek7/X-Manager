"""Module containing the Favorites class for deleting user's favorites"""

import os


class Favorites:
    """Handles management of favorites."""

    _max_delete = os.getenv("MAX_DELETE", None)
    _base_wait_time = float(os.getenv("BASE_WAIT_TIME_FAVORITES", "0.25"))
    _increment_wait = float(os.getenv("INCREMENT_WAIT_FAVORITES", "0.2"))
    _decrement_wait = float(os.getenv("DECREMENT_WAIT_FAVORITES", "0.05"))
    _retry_count = int(os.getenv("RETRY_COUNT_FAVORITES", "3"))
    _rate_limit_window = int(os.getenv("RATE_LIMIT_WINDOW_FAVORITES", f"{15 * 60}"))
    _rate_limit_max_delete = int(os.getenv("RATE_LIMIT_MAX_DELETE", "50"))

    def fetch_likes(self, last_button=None):
        pass

    def fetch_tweet_text(self, button=None):
        pass

    def wait(self, ms):
        pass

    def save_progress(self, count):
        pass

    def load_progress(self):
        pass
