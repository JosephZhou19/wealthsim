from sqlalchemy import Column, ForeignKey, Float
from app.database.database import Base
from sqlalchemy.dialects.postgresql import JSONB

class SimulationResult(Base):
    __tablename__ = "simulation_results"
    run_id = Column(ForeignKey("simulation_runs.id"), primary_key=True)
    final_value_p50 = Column(Float, nullable=False)
    final_value_p25 = Column(Float, nullable=False)
    final_value_p75 = Column(Float, nullable=False)
    final_value_p95 = Column(Float, nullable=False)
    final_value_p5 = Column(Float, nullable=False)
    max_drawdown = Column(Float, nullable=False)
    probability_of_loss = Column(Float, nullable=False)
    metrics = Column(JSONB, nullable=True)