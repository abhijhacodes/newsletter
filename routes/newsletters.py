from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db import schemas
from db.database import get_db_connection
from db.crud.newsletters import create_newsletter, get_newsletters, delete_newsletter_by_id
from db.crud.subscriptions import get_subscriptions
from utils.email import send_email_in_background
from utils.auth import oauth2_scheme, validate_access_token

router = APIRouter(
    prefix="/api/newsletters",
    tags=["Newsletters"]
)


@router.post("/publish")
def publish_newsletter(newsletter: schemas.NewsLetterCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db_connection), token: str = Depends(oauth2_scheme)):
    email_subject = newsletter.title
    email_body = newsletter.body
    allow_unsubscription = newsletter.include_unsubscribe_link or newsletter.include_unsubscribe_link is None

    try:
        validate_access_token(token)
        db_newsletter = create_newsletter(db, newsletter)
        subscribers = get_subscriptions(db)

        for subscriber in subscribers:
            email_reciever = subscriber.email
            subscription_id = subscriber.subscription_id
            background_tasks.add_task(
                send_email_in_background, email_subject, email_body, email_reciever, allow_unsubscription, subscription_id)

        return {"status_code": status.HTTP_200_OK, "message": f"Created your newsletter '{email_subject}' successfully and sent emails.", "newsletter_id": db_newsletter.id}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__str__())


@router.get("/all", response_model=List[schemas.NewsLetterRead])
def get_all_newsletters(db: Session = Depends(get_db_connection), token: str = Depends(oauth2_scheme)):
    try:
        validate_access_token(token)
        newsletters = get_newsletters(db)
        return newsletters
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__str__())


@router.delete("/delete/{newsletter_id}")
def delete_newsletter(newsletter_id: int, db: Session = Depends(get_db_connection), token: str = Depends(oauth2_scheme)):
    newsletter_found = False

    try:
        validate_access_token(token)
        newsletter_title = delete_newsletter_by_id(db, newsletter_id)
        if newsletter_title:
            newsletter_found = True
            return {"message": f"Newsletter '{newsletter_title}' deleted successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__str__())

    if not newsletter_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Newsletter not found")
