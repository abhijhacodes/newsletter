from fastapi import APIRouter

router = APIRouter(
    prefix="/newsletters",
    tags=["Newsletters"]
)


@router.post("/publish")
def publish_newsletter():
    pass
