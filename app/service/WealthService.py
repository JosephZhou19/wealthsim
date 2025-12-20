from app.database.database import SessionLocal
from app.crud import AssetCrud, ContributionRuleCrud
import numpy as np
import logging 
logger = logging.getLogger(__name__)
class WealthService:
    def __init__(self, path: int):
        self.MT_PATHS = path
    @staticmethod
    def simulate_basic_wealth(years: int):
        db = SessionLocal()
        assets = AssetCrud.get_assets(db)
        rules = ContributionRuleCrud.get_rules(db)
        total = 0.0
        asset_totals = {}
        for asset in assets:
            asset_total = 0.0
            after_tax_rate = (asset.expected_return * (1 - asset.tax_drag))/12
            periods = years * 12
            asset_total += asset.initial_value * ((1 + after_tax_rate) ** periods)
            for rule in rules:
                if rule.asset_name == asset.name:
                    asset_total += rule.rate * ((1 + after_tax_rate) ** periods - 1) / (after_tax_rate)
            asset_totals[asset.name] = asset_total
            total += asset_total
        db.close()
        return total, asset_totals
    def simulate_advanced_wealth(self, years: int):
        db = SessionLocal()
        assets = AssetCrud.get_assets(db)
        rules = ContributionRuleCrud.get_rules(db)
        asset_rule_map = {}
        for asset in assets:
            asset_rule_map[asset.name] = []
            for rule in rules:
                if asset.name == rule.asset_name:
                    asset_rule_map[asset.name].append(rule)
        paths = []
        for i in range(self.MT_PATHS):
            paths.append(self.simulate_path(assets, asset_rule_map, years))
        db.close()
        return paths
    def simulate_path(self, assets, asset_rule_map, years):
        portfolio_total = 0.0
        rng = np.random.default_rng()
        for asset in assets:
            asset_total = self.simulate_asset(asset, asset_rule_map[asset.name], years, rng)
            portfolio_total += asset_total
        return portfolio_total
    
    def simulate_asset(self, asset, rules, years, rng: np.random.Generator):
        dt = 1.0 / 12.0
        asset_total = asset.initial_value
        rate = asset.expected_return
        # Simulate monthly growth
        for i in range(years * 12):
            z = rng.normal(0, 1)
            rate_change = rng.normal(0, asset.return_volatility) * np.sqrt(dt)
            rate += rate_change
            rate = max(rate, 0.0)
            logger.info(f"Rate: {rate}")
            growth = np.exp((rate - 0.5 * asset.volatility ** 2) * dt + asset.volatility * np.sqrt(dt) * z)
            new_value = asset_total * growth
            gain = new_value - asset_total
            if gain > 0:
                gain = gain * (1 - asset.tax_drag) 
            asset_total = asset_total + gain + sum([rule.rate for rule in rules])
            logger.info(f"Asset: {asset.name}, Month: {i+1}, Value: {asset_total}")
        return asset_total




        

