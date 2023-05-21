from sqlalchemy.orm import Session
import datetime

from .. import schemas, models


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
