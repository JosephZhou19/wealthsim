from pydantic import BaseModel

class ContributionRuleBase(BaseModel):
    name: str
    rate: float
    asset_name: str

class ContributionRuleCreate(ContributionRuleBase):
    pass

class ContributionRule(ContributionRuleBase):
    class Config:
        orm_mode = True