
from typing import Optional
from fastapi import APIRouter, Query
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.crud import AssetCrud, SimulationCrud, ContributionRuleCrud
from app.service.WealthService import WealthService
from app.service.AIService import AIService

router = APIRouter(
    prefix="/simulate",
    tags=["simulate"],
)

@router.get("/simulationRuns")
def get_simulation_runs():
    db: Session = SessionLocal()
    simulation_runs = SimulationCrud.getSimulationRuns(db)
    db.close()
    return simulation_runs

@router.get("/simulationResults")
def get_simulation_results():
    db: Session = SessionLocal()
    simulation_results = SimulationCrud.getSimulationResults(db)
    db.close()
    return simulation_results

@router.get("/basic/{years}")
def simulate_basic_wealth(years: int):
    total, asset_totals =WealthService.simulate_basic_wealth(years)
    return {"years": years, "total_wealth": total, "asset_totals": asset_totals}

@router.get("/advanced/{years}")
def simulate_advanced_wealth(years: int, seed: Optional[int] = Query(default=None)):
    wealth_service = WealthService(1000)
    result = wealth_service.simulate_advanced_wealth(years, seed)
    db: Session = SessionLocal()
    assets = AssetCrud.get_assets(db)
    rules = ContributionRuleCrud.get_all_rules(db)
    db.close()
    payload = AIService.build_analysis_payload(assets, rules, result)
    ai_response = AIService.generate_ai_analysis(payload)
    result["AI_response"] = ai_response
    return result