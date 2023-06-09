from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from email_validator import validate_email, EmailNotValidError
from typing import List

from db import schemas
from db.database import get_db_connection
from db.crud.subscriptions import check_subscription, create_subscription, delete_subscription, get_subscriptions
from utils.auth import oauth2_scheme, validate_access_token

router = APIRouter(
    prefix="/api/subscriptions",
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
            return {"status_code": status.HTTP_200_OK, "message": "Subscribed to the newsletter successfully", "subscription_id": subscription.subscription_id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__str__())

    if is_already_subscribed:
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You are already subscribed to the newsletter")


@router.delete("/unsubscribe/{subscription_id}")
def unsubscribe_from_newsletter(subscription_id: str, db: Session = Depends(get_db_connection)):
    subscription_found = False

    try:
        unsubscribed_email = delete_subscription(db, subscription_id)
        if unsubscribed_email:
            subscription_found = True
            return {"status_code": status.HTTP_200_OK, "message": "Unsubscribed from newsletter successfully", "email": unsubscribed_email}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=e.__str__())

    if not subscription_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Newsletter subscription not found")


@router.get("/all", response_model=List[schemas.SubscriberRead])
def get_all_subscribers(db: Session = Depends(get_db_connection), token: str = Depends(oauth2_scheme)):
    try:
        validate_access_token(token)
        subscriptions = get_subscriptions(db)
        return subscriptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__str__())
