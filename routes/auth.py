from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from utils.auth import check_credentials, generate_access_token

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/login")
async def login_as_admin(response: Response, formdata: OAuth2PasswordRequestForm = Depends()):
    are_creds_valid = check_credentials(formdata.username, formdata.password)
    if not are_creds_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid username or password")

    access_token = generate_access_token(data={"sub": formdata.username})
    response.set_cookie(key="access_token", value=access_token, httponly=False)
    return {"status_code": status.HTTP_200_OK, "access_token": access_token, "token_type": "bearer"}
