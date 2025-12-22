from fastapi import APIRouter, File, UploadFile
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.schema.AssetBase import AssetCreate
from app.crud import AssetCrud
from app.service.WealthService import WealthService
import csv
import io

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

async def handle_file_upload(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        return {"error": "Invalid file format. Only CSV files are allowed."}
    contents = await file.read()
    decoded_contents = contents.decode('utf-8')
    csv_reader = csv.reader(io.StringIO(decoded_contents))
    data_list = []
    for row in csv_reader:
        data_list.append(float(row[0]))
    return data_list

@router.put("/calculate_volatility/{asset_name}")
async def calculate_volatility(asset_name: str, file:  UploadFile = File(...)):
    return_data = await handle_file_upload(file)
    db: Session = SessionLocal()
    asset = AssetCrud.get_asset(db, asset_name)
    if asset is None:
        return {"error": "Asset not found"}
    volatility = WealthService.calculate_volatility(return_data)
    asset.volatility = volatility
    asset = AssetCrud.update_asset(db, asset_name, asset)
    db.close()
    return asset

@router.put("/calculate_return_volatility/{asset_name}")
async def calculate_return_volatility(asset_name: str, file: UploadFile = File(...)):
    return_data = await handle_file_upload(file)
    print(return_data)
    db: Session = SessionLocal()
    asset = AssetCrud.get_asset(db, asset_name)
    if asset is None:
        return {"error": "Asset not found"}
    return_volatility = WealthService.calculate_volatility(return_data)
    print(return_volatility)
    asset.return_volatility = return_volatility
    asset = AssetCrud.update_asset(db, asset_name, asset)
    db.close()
    return asset

