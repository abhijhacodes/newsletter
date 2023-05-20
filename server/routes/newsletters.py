from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import schemas
from db.database import get_db_connection

router = APIRouter(
    prefix="/api/newsletters",
    tags=["Newsletters"]
)


@router.post("/publish")
def publish_newsletter(newsletter: schemas.NewsLetterCreate, db: Session = Depends(get_db_connection)):
    return {"lol": newsletter.title}
