from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.crud import ProfileCrud
from app.schema.ProfileBase import ProfileCreate

router = APIRouter(
    prefix="/profile",
    tags=["profile"],
)

@router.post("/")
def create_profile(newProfile: ProfileCreate):
    db: Session = SessionLocal()
    response = ProfileCrud.create_profile(db, newProfile)
    db.close()
    return response
@router.get("/")
def get_profile():
    db: Session = SessionLocal()
    profile = ProfileCrud.get_profile(db)
    db.close()
    return profile