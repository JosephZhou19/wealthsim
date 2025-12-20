from pydantic import BaseModel

class AssetBase(BaseModel):
    name: str
    initial_value: float
    expected_return: float
    tax_drag: float
    volatility: float
    return_volatility: float

class AssetCreate(AssetBase):
    pass

class Asset(AssetBase):
    class Config:
        orm_mode = True