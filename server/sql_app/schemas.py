import datetime
from pydantic import BaseModel


class SubscriberBase(BaseModel):
    subscription_id: str
    email: str


class Subscriber(SubscriberBase):
    id: int
    subscribed_at: datetime

    class Config:
        orm_mode = True


class NewsLetterBase(BaseModel):
    title: str
    body: str
    published_by: str
    include_unsubscribe_link: bool = True


class NewsLetter(NewsLetterBase):
    id: int
    published_at: datetime

    class Config:
        orm_mode = True
