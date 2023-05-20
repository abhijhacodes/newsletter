from fastapi import APIRouter, Depends, HTTPException, status
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.orm import Session
from db import schemas
from db.database import get_db_connection
from db.crud import create_subscription, delete_subscription, get_subscriptions, check_subscription

router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"]
)


@router.post("/subscribe")
def subscribe_to_newsletter(subscriber: schemas.SubscriberCreate, db: Session = Depends(get_db_connection)):
    email = subscriber.email
    is_already_subscribed = False

    if not email or not len(email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Please provide an email id")

    try:
        validate_email(email)
    except EmailNotValidError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Please provide valid email id")

    try:
        if check_subscription(db, subscriber):
            is_already_subscribed = True
        else:
            subscription = create_subscription(db, subscriber)
            return {"message": "Subscribed to the newsletter successfully", "subscription_id": subscription.subscription_id}
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong, please try again.")

    if is_already_subscribed:
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You are already subscribed to the newsletter")


@router.get("/unsubscribe/{subscription_id}")
def unsubscribe_from_newsletter(subscription_id: str, db: Session = Depends(get_db_connection)):
    subscription_found = False

    try:
        unsubscribed_email = delete_subscription(db, subscription_id)
        if unsubscribed_email:
            subscription_found = True
            return {"message": "Unsubscribed from newsletter successfully", "email": unsubscribed_email}
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong, please try again.")

    if not subscription_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Newsletter subscription not found")


@router.get("/all", response_model=list[schemas.SubscriberRead])
def get_all_subscribers(db: Session = Depends(get_db_connection)):
    return get_subscriptions(db)
