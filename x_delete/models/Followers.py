from beanie import Document


class Follower(Document):
    accountId: str
    userLink: str
