from sqlalchemy import Column, String, DateTime, UUID, BigInteger, func, Integer
from app.database.database import Base
import uuid

class SimulationRun(Base):
    __tablename__ = "simulation_runs"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    period = Column(Integer, nullable=False)
    seed = Column(String, nullable=False)
    num_simulations = Column(Integer, nullable=False)
    create_dttm = Column(DateTime, server_default=func.now())
