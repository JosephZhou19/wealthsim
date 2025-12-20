from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.schema.AssetBase import AssetCreate
from app.crud import AssetCrud
from app.service.WealthService import WealthService

router = APIRouter(
    prefix="/assets",
    tags=["assets"],
)


@router.post("/")
def create_asset(newAsset: AssetCreate):
    db: Session = SessionLocal()
    response = AssetCrud.create_asset(db, newAsset)
    db.close()
    return response

@router.get("/")
def get_assets():
    db: Session = SessionLocal()
    assets = AssetCrud.get_assets(db)
    db.close()
    return assets
@router.delete("/{asset_name}")
def delete_asset(asset_name: str):
    db: Session = SessionLocal()
    asset = AssetCrud.delete_asset(db, asset_name)
    db.close()
    return asset
@router.put("/{asset_name}")
def update_asset(asset_name: str, updated_asset: AssetCreate):
    db: Session = SessionLocal()
    asset = AssetCrud.update_asset(db, asset_name, updated_asset)
    db.close()
    return asset

