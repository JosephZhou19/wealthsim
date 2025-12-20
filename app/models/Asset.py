from sqlalchemy import Column, String, Float
from app.database.database import Base

class Asset(Base):
    __tablename__ = "assets"

    name = Column(String, primary_key=True, nullable=False)
    initial_value = Column(Float, nullable=False)
    expected_return = Column(Float, nullable=False)
    tax_drag = Column(Float, nullable=False)
    volatility = Column(Float, nullable=False)
    return_volatility = Column(Float, nullable=False)
