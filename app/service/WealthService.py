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
        wealth_totals = [path[0] for path in paths]
        p25 = np.percentile(wealth_totals, 25)
        p75 = np.percentile(wealth_totals, 75)
        p50 = np.percentile(wealth_totals, 50)
        p5 = np.percentile(wealth_totals, 5)
        p95 = np.percentile(wealth_totals, 95)
        max_drawdown = max([path[1] for path in paths])
        probability_of_loss = sum([path[2] for path in paths]) / len(paths)
        db.close()
        return {
            "p5": p5,
            "p25": p25,
            "p50": p50,
            "p75": p75,
            "p95": p95,
            "max_drawdown": max_drawdown,
            "probability_of_loss": probability_of_loss
        }
    def simulate_path(self, assets, asset_rule_map, years):
        portfolio_total = 0.0
        peak = sum([asset.initial_value for asset in assets])
        max_drawdown = 0.0
        rng = np.random.default_rng()
        no_growth_total = peak
        isLoss = False
        # Simulate monthly growth
        for i in range(years * 12):
            for asset in assets:
                asset_total = self.simulate_asset_growth(asset, asset_rule_map[asset.name], rng)
                portfolio_total += asset_total
            # calculate draw down
            peak = max(peak, portfolio_total)
            drawdown = (peak - portfolio_total) / peak
            max_dd = max(max_drawdown, drawdown)
            for asset in assets:
                asset_contribution = sum([rule.rate for rule in asset_rule_map[asset.name]])
                portfolio_total += asset_contribution
                no_growth_total += asset_contribution   
        if no_growth_total > portfolio_total:
            isLoss = True
        return portfolio_total, max_dd, isLoss
    
    def simulate_asset_growth(self, asset, rules, rng: np.random.Generator):
        dt = 1.0 / 12.0
        asset_total = asset.initial_value
        rate = asset.expected_return
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
        logger.info(f"Asset: {asset.name}, Value: {asset_total}")
        return asset_total




        

