"""Holds the Router route for connecting to websocket"""

import logging
import json
from fastapi import WebSocket, WebSocketDisconnect
from faststream.rabbit import RabbitQueue
from pydantic.types import Json
from x_manager.ws_manager import WebSocketManager
from x_manager.routers.rabbit.setup import RabbitMQManager

LOGGER = logging.Logger("__name__")
router = RabbitMQManager().router


@router.websocket("/ws", name="Connect to WebSocket")
async def connect_to_ws_route(websocket: WebSocket):
    """Main WebSocket Connection Route"""
    wsm = WebSocketManager()
    await wsm.connect(websocket)
    try:
        while True:
            data: Json = await websocket.receive_json()
            dic = json.loads(data)
            LOGGER.info("Message Received for queue: %s", dic["queue"])
            queue = RabbitQueue(name=dic["queue"])
            # We're going to push it off to RabbitMQ queues to not clutter this up
            await router.broker.publish(message=data, queue=queue)
    except WebSocketDisconnect:
        LOGGER.info(msg="WebSocket has been disconnected.")
