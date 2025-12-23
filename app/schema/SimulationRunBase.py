from pydantic import BaseModel

class SimulationRunBase(BaseModel):
    period: int
    seed: str
    num_simulations: int

class SimulationRunCreate(SimulationRunBase):
    pass

class SimulationRun(SimulationRunBase):
    class Config:
        orm_mode = True