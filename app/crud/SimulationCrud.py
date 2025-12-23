from sqlalchemy.orm import Session

from app.schema.SimulationResultBase import SimulationResultCreate
from app.schema.SimulationRunBase import SimulationRunCreate
from app.models.SimulationRun import SimulationRun
from app.models.SimulationResult import SimulationResult
def createSimulationRun(db: Session, simulationRun: SimulationRunCreate):
    db_simulation_run = SimulationRun(
        period=simulationRun.period,
        seed=simulationRun.seed,
        num_simulations=simulationRun.num_simulations,
    )
    db.add(db_simulation_run)
    db.commit()
    db.refresh(db_simulation_run)
    return db_simulation_run

def createSimulationResult(db: Session, simulationResult: SimulationResultCreate):
    db_simulation_result = SimulationResult(
        run_id=simulationResult.run_id,
        final_value_p50=simulationResult.final_value_p50,
        final_value_p25=simulationResult.final_value_p25,
        final_value_p75=simulationResult.final_value_p75,
        final_value_p5=simulationResult.final_value_p5,
        final_value_p95=simulationResult.final_value_p95,
        max_drawdown=simulationResult.max_drawdown,
        probability_of_loss=simulationResult.probability_of_loss,
        metrics=simulationResult.metrics
    )
    db.add(db_simulation_result)
    db.commit()

def getSimulationRuns(db: Session):
    return db.query(SimulationRun).all()
def getSimulationResults(db: Session):
    return db.query(SimulationResult).all()