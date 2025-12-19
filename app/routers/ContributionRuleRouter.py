from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.schema.ContributionRuleBase import ContributionRuleCreate
from app.crud import ContributionRuleCrud


router = APIRouter(
    prefix="/ContributionRules",
    tags=["contribution_rules"],
)



@router.post("/")
def create_rule(newRule: ContributionRuleCreate):
    db: Session = SessionLocal()
    rule = ContributionRuleCrud.create_contribution_rule(db, newRule)
    db.close()
    return rule

@router.get("/")
def get_rules():
    db: Session = SessionLocal()
    rule = ContributionRuleCrud.get_rules(db)
    db.close()
    return rule
@router.delete("/{rule_name}")
def delete_rule(rule_name: str):
    db: Session = SessionLocal()
    rule = ContributionRuleCrud.delete_contribution_rule(db, rule_name)
    db.close()
    return rule

@router.put("/{rule_name}")
def update_rule(rule_name: str, updated_rule: ContributionRuleCreate):
    db: Session = SessionLocal()
    rule = ContributionRuleCrud.update_contribution_rule(db, rule_name, updated_rule)
    db.close()
    return rule
