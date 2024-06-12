from beanie import Document


class Like(Document):
    tweetId: str
    fullText: str
    expandedUrl: str
