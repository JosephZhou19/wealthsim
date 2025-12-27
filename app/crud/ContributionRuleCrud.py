from sqlalchemy.orm import Session
from app.models.ContributionRule import ContributionRule
from app.schema.ContributionRuleBase import ContributionRuleCreate


def create_contribution_rule(db: Session, contribution_rule: ContributionRuleCreate):
    db_rule =  ContributionRule(
        name=contribution_rule.name,
        rate=contribution_rule.rate,
        asset_name=contribution_rule.asset_name
        )
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

def get_rules(db: Session, asset_name: str):
    return db.query(ContributionRule).filter(ContributionRule.asset_name==asset_name).all()
def delete_contribution_rule(db: Session, rule_name: str):
    db_rule = db.query(ContributionRule).filter(ContributionRule.name == rule_name).first()
    if db_rule:
        db.delete(db_rule)
        db.commit()
    return db_rule
def update_contribution_rule(db: Session, rule_name: str, updated_rule: ContributionRuleCreate):
    db_rule = db.query(ContributionRule).filter(ContributionRule.name == rule_name).first()
    if db_rule:
        db_rule.rate = updated_rule.rate
        db.commit()
        db.refresh(db_rule)
    return db_rule