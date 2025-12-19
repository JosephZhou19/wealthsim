from sqlalchemy import Column, String, Float, ForeignKey
from app.database.database import Base

class ContributionRule(Base):
    __tablename__ = "contribution_rules"

    name = Column(String, primary_key=True, nullable=False)
    rate = Column(Float, nullable=False)
    asset_name = Column(ForeignKey("assets.name"), nullable=False)

