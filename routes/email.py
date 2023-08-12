import os
from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from email_validator import validate_email, EmailNotValidError
from utils.email import send_email_in_background
from db import schemas

router = APIRouter(
    prefix="/api/email",
    tags=["Email"]
)


@router.post("/send")
async def send_email(email_body: schemas.EmailSend, background_tasks: BackgroundTasks):
    email_api_key = os.environ['EMAIL_API_KEY']
    if email_body.api_key != email_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid api key")

    subject = email_body.subject
    body = email_body.body
    reciever = email_body.reciever

    try:
        validate_email(reciever)
    except EmailNotValidError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email id is not valid")

    try:
        background_tasks.add_task(send_email_in_background,
                                  subject, body, reciever, False, None, True)
        return {"status_code": status.HTTP_200_OK, "message": "Email sent successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__str__())
