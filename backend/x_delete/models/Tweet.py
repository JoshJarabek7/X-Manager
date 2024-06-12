"""Contains the Beanie Document models for Tweets"""

from datetime import datetime
from typing import List, Optional
from beanie import Document, PydanticObjectId
from pydantic import BaseModel
from archive import ArchiveExtract


class EditInfo(BaseModel):
    """EditInfo Nested Document for Tweet Document"""

    editTweetIds: List[str]
    editableUntil: datetime
    editsRemaining: int
    isEditEligible: bool


class UserMention(BaseModel):
    """UserMention Nested Document for Tweet Document"""

    name: str
    screen_name: str
    indices: List[int]
    id_str: Optional[str]
    id: Optional[PydanticObjectId]


class Entities(BaseModel):
    """Entities Nested Document for Tweet Document"""

    hashtags: List[str]
    symbols: List[str]
    user_mentions: List[UserMention]
    urls: List[str]


class Tweet(Document):
    """Beanie document model for tweets"""

    edit_info: EditInfo
    retweeted: bool
    source: str
    entities: Entities
    display_text_range: List[int]
    favorite_count: int
    in_reply_to_status_id_str: Optional[str]
    id_str: str
    in_reply_to_user_id: Optional[int]
    truncated: bool
    retweet_count: int
    in_reply_to_status_id: Optional[int]
    created_at: datetime
    favorited: bool
    full_text: str
    lang: str
    in_reply_to_screen_name: Optional[str]
    in_reply_to_user_id_str: Optional[str]
