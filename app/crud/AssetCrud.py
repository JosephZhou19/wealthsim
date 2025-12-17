from sqlalchemy.orm import Session
from app.models.Asset import Asset
from app.schema.AssetBase import AssetCreate

def create_asset(db: Session, asset: AssetCreate):
    db_asset = Asset(
        name=asset.name,
        initial_value=asset.initial_value,
        expected_return=asset.expected_return,
        tax_drag=asset.tax_drag
        )
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

def get_assets(db: Session):
    return db.query(Asset).all()
def delete_asset(db: Session, asset_name: str):
    asset = db.query(Asset).filter(Asset.name == asset_name).first()
    if asset:
        db.delete(asset)
        db.commit()
    return asset
def update_asset(db: Session, asset_name: str, updated_asset: AssetCreate):
    asset = db.query(Asset).filter(Asset.name == asset_name).first()
    if asset:
        asset.initial_value = updated_asset.initial_value
        asset.expected_return = updated_asset.expected_return
        asset.tax_drag = updated_asset.tax_drag
        db.commit()
        db.refresh(asset)
    return asset