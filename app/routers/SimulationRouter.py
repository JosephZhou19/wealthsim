
from typing import Optional
from fastapi import APIRouter, Query
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.crud import AssetCrud, SimulationCrud, ContributionRuleCrud, ProfileCrud
from app.models.SimulationResult import SimulationResult
from app.schema.ChatBase import ChatRequest
from app.service.WealthService import WealthService
from app.service.AIService import AIService
import uuid

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
    return result

@router.post("/aiChat")
def chat(request: ChatRequest):
    db: Session = SessionLocal()
    profile = ProfileCrud.get_profile(db)
    run_id = uuid.UUID(request.run_id)
    simulation_result = SimulationCrud.getSimulationResult(db, run_id)
    simulation_run = SimulationCrud.getSimulationRun(db, run_id)
    assets = AssetCrud.get_assets(db)
    rules = ContributionRuleCrud.get_all_rules(db)
    system_prompt = AIService.build_analysis_payload(assets, rules, simulation_run, simulation_result, profile)
    return AIService.generate_ai_analysis(system_prompt, request.messages)