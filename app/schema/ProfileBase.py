from pydantic import BaseModel

class ProfileBase(BaseModel):
    name: str
    horizon_years: int
    primary_objective: str
    risk_attitude: str
    income_stability: str
    class Config:
        from_attributes = True

class ProfileCreate(ProfileBase):
    pass

class Profile(ProfileBase):
    class Config:
        orm_mode = True