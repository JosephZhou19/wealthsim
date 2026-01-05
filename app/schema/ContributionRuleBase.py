from pydantic import BaseModel

class ContributionRuleBase(BaseModel):
    name: str
    rate: float
    asset_name: str
    class Config:
        from_attributes = True

class ContributionRuleCreate(ContributionRuleBase):
    pass

class ContributionRule(ContributionRuleBase):
    class Config:
        orm_mode = True