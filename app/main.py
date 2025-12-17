from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.database import engine, SessionLocal, Base
from app.models.Asset import Asset
from app.schema.AssetBase import AssetCreate
from app.crud import AssetCrud

app = FastAPI()

# Create tables automatically on startup
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.post("/assets")
def create_asset(newAsset: AssetCreate):
    db: Session = SessionLocal()
    response = AssetCrud.create_asset(db, newAsset)
    db.close()
    return response

@app.get("/assets")
def get_assets():
    db: Session = SessionLocal()
    assets = AssetCrud.get_assets(db)
    db.close()
    return assets
@app.delete("/assets/{asset_name}")
def delete_asset(asset_name: str):
    db: Session = SessionLocal()
    asset = AssetCrud.delete_asset(db, asset_name)
    db.close()
    return asset
@app.put("/assets/{asset_name}")
def update_asset(asset_name: str, updated_asset: AssetCreate):
    db: Session = SessionLocal()
    asset = AssetCrud.update_asset(db, asset_name, updated_asset)
    db.close()
    return asset
