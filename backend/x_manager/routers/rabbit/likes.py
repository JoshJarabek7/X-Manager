"""Contains RabbitMQ Routes for Likes"""

import json
from x_manager.routers.apis.ws import WebSocketManager
from x_manager.models.Likes import Like
from x_manager.likes import Likes
from pydantic import BaseModel
from beanie import PydanticObjectId
from .manager import RabbitMQManager

router = RabbitMQManager().router


class DeleteLikeSchema(BaseModel):
    """Schema for deleting a single like"""

    queue: str
    like_id: str


class DeleteLikesSchema(BaseModel):
    """Schema for deleting multiple likes"""

    queue: str
    like_ids: list[str]


@router.subscriber(queue="CLIENT.LIKE.DELETE")
async def inform_client_like_was_deleted(m: DeleteLikeSchema):
    """Let client know that a specific like_id was deleted successfully"""
    wsm = WebSocketManager()
    d = {"category": "likes", "action": "delete", "id": m.like_id}
    j = json.dumps(d)
    await wsm.send(data=j)


@router.subscriber(queue="DB.LIKE.DELETE")
async def delete_like_id(m: DeleteLikeSchema):
    """Receive task to delete like of like_id from database"""
    bson_id = PydanticObjectId(m.like_id)
    like_document = await Like.get(bson_id)
    if like_document:
        await like_document.delete()
    data_schema = DeleteLikeSchema(queue="CLIENT.LIKE.DELETE", like_id=m.like_id)
    j = data_schema.model_dump_json()
    await router.broker.publish(message=j, queue="CLIENT.LIKE.DELETE")


@router.subscriber(queue="DB.LIKES.DELETE")
async def delete_like_ids(m: DeleteLikesSchema):
    """Receive an array of like_ids to delete from database"""
    likes = m.like_ids

    for like in likes:
        d = DeleteLikeSchema(queue="CLIENT.LIKE.DELETE", like_id=like)
        j = d.model_dump_json()
        await router.broker.publish(message=j, queue="DB.LIKE.DELETE")


@router.subscriber(queue="DRIVER.LIKE.DELETE")
async def driver_delete_like_ids(m: DeleteLikesSchema):
    """Receive an array of like_ids to delete from X"""
    likes = m.like_ids
    likes_manager = Likes()

    for like in likes:
        await likes_manager.delete(like)
