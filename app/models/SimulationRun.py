from sqlalchemy import Column, String, DateTime, UUID, BigInteger, func
from app.database.database import Base
import uuid

class SimulationRun(Base):
    __tablename__ = "simulation_runs"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, defaultuu= uuid.uuid4)
    period = Column(int, nullable=False)
    seed = Column(BigInteger, nullable=False)
    num_simulations = Column(int, nullable=False)
    create_dttm = Column(DateTime, server_default=func.now())
