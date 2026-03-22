from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash
from app.db.models import User
from app.db.session import SessionLocal


def bootstrap_admin_user() -> None:
    db: Session = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == settings.bootstrap_admin_username).first()
        if existing:
            return

        user = User(
            username=settings.bootstrap_admin_username,
            email=settings.bootstrap_admin_email,
            hashed_password=get_password_hash(settings.bootstrap_admin_password),
            is_active=True,
        )
        db.add(user)
        db.commit()
    finally:
        db.close()
