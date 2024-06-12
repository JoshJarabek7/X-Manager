"""Module containing the WebSocket Manager Singleton class"""

from fastapi import WebSocket
from pydantic.types import Json


class WebSocketManager:
    """Singleton class that stores the WebSocket connection to the frontend"""

    _ws: WebSocket

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(WebSocketManager, cls).__new__(cls)
        return cls.instance

    @property
    def connection(self) -> WebSocket:
        """Represents the existing WebSocket Connection

        Raises:
            AttributeError: Raises an AttributeError if WebSocket connection missing.

        Returns:
            WebSocket: Return instance of WebSocket connection if exists
        """
        if self._ws:
            return self._ws
        raise AttributeError

    async def send(self, data: Json):
        """Sends JSON data to client.

        Args:
            data (JSON): JSON data to send to client
        """
        await self._ws.send_json(data)

    async def connect(self, ws: WebSocket) -> None:
        """Accepts WebSocket Connection and stores the connection in the _ws attribute

        Args:
            ws (WebSocket): WebSocket connection to the frontend
        """
        self._ws = ws
        await self._ws.accept()
