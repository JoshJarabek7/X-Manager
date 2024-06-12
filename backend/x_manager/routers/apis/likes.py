from fastapi import APIRouter
from pydantic import BaseModel
from beanie import PydanticObjectId

router = APIRouter()


class DeleteLikesSchema(BaseModel):
    likes: list[PydanticObjectId]


@router.get("/likes")
async def get_likes_route():
    pass


@router.delete("/likes")
async def delete_likes_route(likes_to_delete: DeleteLikesSchema):
    pass
