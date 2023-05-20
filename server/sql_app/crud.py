import datetime
from sqlalchemy.orm import Session
from . import schemas, models
import uuid


def create_subscription(db: Session, subscription_body: schemas.SubscriberCreate):
    subscription_id = str(uuid.uuid4())[:8]
    subscribed_at = datetime.datetime.now()

    db_subscription = models.Subscriber(
        subscription_id=subscription_id, email=subscription_body.email, subscribed_at=subscribed_at)
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription


def delete_subscription(db: Session, unsubscription_body: schemas.SubscriberDelete):
    subscription = db.query(models.Subscriber).filter(
        models.Subscriber.subscription_id == unsubscription_body.subscription_id).first()
    email = subscription.email

    if subscription:
        db.delete(subscription)
        db.commit()
        return email
    return None


def create_newsletter(db: Session, newsletter_body: schemas.NewsLetterCreate):
    published_at = datetime.datetime.now()

    db_newsletter = models.NewsLetter(
        title=newsletter_body.title, body=newsletter_body.body, published_by=newsletter_body.published_by, include_unsubscribe_link=newsletter_body.include_unsubscribe_link, published_at=published_at)
    db.add(db_newsletter)
    db.commit()
    db.refresh(db_newsletter)
    return db_newsletter
