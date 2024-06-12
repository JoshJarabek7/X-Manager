"""Module containing the Likes class for deleting user's likes"""

import os
import datetime
import asyncio
from selenium.webdriver.common.by import By
from pydantic import BaseModel
from x_manager.navigator import Navigator
from x_manager.driver import DriverManager
from x_manager.routers.rabbit.manager import RabbitMQManager


class RabbitMessage(BaseModel):
    """Schema for sending and receiving basic RabbitMQ Messages"""

    queue: str
    like_id: str


class Likes:
    """Handles management of likes."""

    _max_delete = os.getenv("MAX_DELETE", None)
    _base_wait_time = float(os.getenv("BASE_WAIT_TIME_LIKES", "0.25"))
    _increment_wait = float(os.getenv("INCREMENT_WAIT_LIKES", "0.2"))
    _decrement_wait = float(os.getenv("DECREMENT_WAIT_LIKES", "0.05"))
    _retry_count = int(os.getenv("RETRY_COUNT_LIKES", "3"))
    _rate_limit_window = int(os.getenv("RATE_LIMIT_WINDOW_LIKES", f"{15 * 60}"))
    _rate_limit_max_delete = int(os.getenv("RATE_LIMIT_MAX_DELETE", "50"))
    _current_window_start_time: datetime.datetime
    _current_window_end_time: datetime.datetime
    _current_window_deletion_count = 0

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Likes, cls).__new__(cls)
            cls._current_window_start_time = datetime.datetime.now()
            cls._current_window_end_time = (
                cls._current_window_start_time
                + datetime.timedelta(seconds=cls._rate_limit_window)
            )
        return cls.instance

    def _get_unlike_button(self):
        driver = DriverManager().driver
        button = driver.find_element(By.XPATH, '//*[@data-testid="unlike"]')
        return button

    def _parse_id_from_url(self, url: str) -> str:
        return url.split("/")[-1]

    async def _send_success_message(self, like_id: str):
        router = RabbitMQManager().router
        queue_name = "DB.LIKE.DELETE"

        m = RabbitMessage(queue=queue_name, like_id=like_id)
        j = m.model_dump_json()
        await router.broker.publish(message=j, queue=queue_name)

    async def _convert_id_to_url(self, like_id: str) -> str:
        return f"https://x.com/i/web/status/{like_id}"

    async def delete(self, like_id: str):
        """Delete like from X"""
        url = await self._convert_id_to_url(like_id)
        await (
            self._within_limits()
        )  # Either returns True or sleeps until it can return True
        self._current_window_deletion_count += 1
        self._go_to_url(url)
        await asyncio.sleep(self._base_wait_time)
        button = self._get_unlike_button()
        button.click()
        like_id = self._parse_id_from_url(url=url)
        await self._send_success_message(like_id=like_id)

    def _go_to_url(self, url):
        navi = Navigator()
        navi.link(url)

    async def _within_limits(self):
        if self._current_window_deletion_count >= self._rate_limit_max_delete:
            if self._current_window_end_time <= datetime.datetime.now():
                self._current_window_start_time = datetime.datetime.now()
                self._current_window_end_time = (
                    self._current_window_start_time
                    + datetime.timedelta(seconds=self._rate_limit_window)
                )
                self._current_window_deletion_count = 0
                return True
            sleep_until = self._current_window_end_time - datetime.datetime.now()
            await asyncio.sleep(
                sleep_until.seconds + 60
            )  # Add 60 seconds to spread out bulk deletions
            return self._within_limits()
        return True
