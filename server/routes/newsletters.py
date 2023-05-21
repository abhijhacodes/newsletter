from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session


from db import schemas
from db.database import get_db_connection
from db.crud import get_subscriptions, create_newsletter
from utils.email import send_email_in_background


router = APIRouter(
    prefix="/api/newsletters",
    tags=["Newsletters"]
)


@router.post("/publish")
def publish_newsletter(newsletter: schemas.NewsLetterCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db_connection)):
    email_subject = newsletter.title
    email_body = newsletter.body
    allow_unsubscription = newsletter.include_unsubscribe_link

    try:
        db_newsletter = create_newsletter(db, newsletter)
        subscribers = get_subscriptions(db)

        for subscriber in subscribers:
            email_reciever = subscriber.email
            subscription_id = subscriber.subscription_id
            background_tasks.add_task(
                send_email_in_background, email_subject, email_body, email_reciever, allow_unsubscription, subscription_id)

        return {"message": f"Created your newsletter {email_subject} successfully and sent emails.", "newsletter_id": db_newsletter.id}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong while sending emails")
