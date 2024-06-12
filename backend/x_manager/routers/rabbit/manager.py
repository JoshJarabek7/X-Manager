"""Module containing RabbitMQManager Singleton class"""

import os
from faststream.rabbit.fastapi import RabbitRouter

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")

router = RabbitRouter(RABBITMQ_URL)


class RabbitMQManager:
    """Manages the RabbitMQ Router"""

    _rabbitmq_url: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
    _router: RabbitRouter

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(RabbitMQManager, cls).__new__(cls)
            cls._router = RabbitRouter(cls._rabbitmq_url)
        return cls.instance

    @property
    def router(self) -> RabbitRouter:
        """Returns RabbitMQ Router"""
        return self._router
