from uuid import UUID
from pydantic import BaseModel

class SimulationResultBase(BaseModel):
    run_id: UUID
    final_value_p50: float
    final_value_p25: float
    final_value_p75: float
    final_value_p95: float
    final_value_p5: float
    max_drawdown: float
    probability_of_loss: float
    metrics: dict

class SimulationResultCreate(SimulationResultBase):
    pass

class SimulationResult(SimulationResultBase):
    class Config:
        orm_mode = True