
from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.schema.AssetBase import AssetCreate
from app.crud import AssetCrud
from app.service.WealthService import WealthService

router = APIRouter(
    prefix="/simulate",
    tags=["simulate"],
)

@router.get("/basic/{years}")
def simulate_basic_wealth(years: int):
    total, asset_totals =WealthService.simulate_basic_wealth(years)
    return {"years": years, "total_wealth": total, "asset_totals": asset_totals}
@router.get("/advanced/{years}")
def simulate_advanced_wealth(years: int):
    wealth_service = WealthService(10)
    paths = wealth_service.simulate_advanced_wealth(years)
    return {"years": years, "paths": paths}