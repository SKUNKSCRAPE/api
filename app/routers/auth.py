from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.db.models import User
from app.deps import get_db
from app.schemas.auth import LoginResponse, UserOut

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=LoginResponse, summary="Authenticate and return JWT")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> LoginResponse:
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(
        subject=user.username,
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserOut.model_validate(user),
    )
