from sqlalchemy.orm import Session
from app.models.Profile import Profile
from app.schema.ProfileBase import ProfileCreate


def create_profile(db: Session, newProfile: ProfileCreate):
    profile = db.query(Profile).first()
    if not profile:
        profile = Profile(
            name=newProfile.name,
            horizon_years=newProfile.horizon_years,
            primary_objective=newProfile.primary_objective,
            risk_attitude=newProfile.risk_attitude,
            income_stability=newProfile.income_stability
        )
        db.add(profile)
    else:
        profile.name = newProfile.name
        profile.horizon_years = newProfile.horizon_years
        profile.primary_objective = newProfile.primary_objective
        profile.risk_attitude = newProfile.risk_attitude
        profile.income_stability = newProfile.income_stability
    db.commit()
    db.refresh(profile)
    return profile
def get_profile(db: Session):
    return db.query(Profile).first()