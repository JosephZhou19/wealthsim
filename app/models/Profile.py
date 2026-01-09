from sqlalchemy import Column, String, Integer
from app.database.database import Base

class Profile(Base):
    __tablename__ = "profile"

    name = Column(String, primary_key=True, nullable=False)
    horizon_years = Column(Integer, nullable=False)
    primary_objective = Column(String, nullable=False)
    risk_attitude = Column(String, nullable=False)
    income_stability = Column(String, nullable=False)

