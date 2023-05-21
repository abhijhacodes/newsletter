import datetime
from pydantic import BaseModel
from typing import Optional


class SubscriberBase(BaseModel):
    email: str


class SubscriberCreate(SubscriberBase):
    pass


class SubscriberRead(SubscriberBase):
    subscription_id: str


class Subscriber(SubscriberBase):
    id: int
    subscription_id: str
    subscribed_at: datetime.datetime

    class Config:
        orm_mode = True


class NewsLetterBase(BaseModel):
    title: str
    body: str
    published_by: str
    include_unsubscribe_link: Optional[bool] = True


class NewsLetterCreate(NewsLetterBase):
    pass


class NewsLetterRead(NewsLetterBase):
    id: int
    published_at: datetime.datetime


class NewsLetter(NewsLetterRead):

    class Config:
        orm_mode = True
