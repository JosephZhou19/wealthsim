from sqlalchemy import Column, ForeignKey
from app.database.database import Base
from sqlalchemy.dialects.postgresql import JSONB

class SimulationResult(Base):
    __tablename__ = "simulation_results"
    run_id = Column(ForeignKey("simulation_runs.id"), primary_key=True)
    final_value_p50 = Column(float, nullable=False)
    final_value_p25 = Column(float, nullable=False)
    final_value_p75 = Column(float, nullable=False)
    final_value_p95 = Column(float, nullable=False)
    final_value_p5 = Column(float, nullable=False)
    max_drawdown = Column(float, nullable=False)
    probabilty_of_loss = Column(float, nullable=False)
    metrics = Column(JSONB, nullable=True)