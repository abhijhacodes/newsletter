from sqlalchemy.orm import Session
import datetime
import uuid

from . import schemas, models


def check_subscription(db: Session, subscription_body: schemas.SubscriberCreate):
    subscription = db.query(models.Subscriber).filter(
        models.Subscriber.email == subscription_body.email).first()
    if subscription:
        return True
    return False


def create_subscription(db: Session, subscription_body: schemas.SubscriberCreate):
    subscription_id = str(uuid.uuid4())[:8]
    subscribed_at = datetime.datetime.now()

    db_subscription = models.Subscriber(
        subscription_id=subscription_id, email=subscription_body.email, subscribed_at=subscribed_at)
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription


def delete_subscription(db: Session, subscription_id: str):
    subscription = db.query(models.Subscriber).filter(
        models.Subscriber.subscription_id == subscription_id).first()

    if subscription:
        email = subscription.email
        db.delete(subscription)
        db.commit()
        return email

    return None


def get_subscriptions(db: Session):
    subscriptions = db.query(models.Subscriber).all()
    return [schemas.SubscriberRead(**subscription.__dict__) for subscription in subscriptions]


def create_newsletter(db: Session, newsletter_body: schemas.NewsLetterCreate):
    published_at = datetime.datetime.now()

    db_newsletter = models.NewsLetter(
        title=newsletter_body.title, body=newsletter_body.body, published_by=newsletter_body.published_by, include_unsubscribe_link=newsletter_body.include_unsubscribe_link, published_at=published_at)
    db.add(db_newsletter)
    db.commit()
    db.refresh(db_newsletter)
    return db_newsletter


def get_newsletters(db: Session):
    newsletters = db.query(models.NewsLetter).all()
    return [schemas.NewsLetterRead(**newsletter.__dict__) for newsletter in newsletters]


def delete_newsletter_by_id(db: Session, newsletter_id: int):
    newsletter = db.query(models.NewsLetter).filter(
        models.NewsLetter.id == newsletter_id).first()

    if newsletter:
        title = newsletter.title
        db.delete(newsletter)
        db.commit()
        return title

    return None
