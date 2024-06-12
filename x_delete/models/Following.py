from beanie import Document


class Following(Document):
    accountId: str
    userLink: str
