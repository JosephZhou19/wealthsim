from app.database.database import SessionLocal
from app.crud import AssetCrud, ContributionRuleCrud
class WealthService:
    @staticmethod
    def simulate_wealth(years: int):
        db = SessionLocal()
        assets = AssetCrud.get_assets(db)
        rules = ContributionRuleCrud.get_rules(db)
        total = 0.0
        asset_totals = {}
        for asset in assets:
            asset_total = 0.0
            after_tax_rate = asset.expected_return * (1 - asset.tax_drag)
            asset_total += asset.initial_value * ((1 + after_tax_rate) ** years)
            for rule in rules:
                if rule.asset_name == asset.name:
                    asset_total += rule.rate * ((1 + after_tax_rate) ** years - 1) / (after_tax_rate)
            asset_totals[asset.name] = asset_total
            total += asset_total
        db.close()
        return total, asset_totals