from app.database.database import SessionLocal
from app.crud import AssetCrud, ContributionRuleCrud
from app.models.Asset import Asset
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
    @staticmethod
    def calculate_volatility(returns: list):
        std_dev = np.std(returns)
        # Assuming returns are monthly
        volatility = std_dev * np.sqrt(12)
        return float(volatility)
    @staticmethod
    def create_asset_copy(assets):
        assets_copy = []
        for asset in assets:
            assets_copy.append(Asset(name=asset.name, initial_value=asset.initial_value, expected_return=asset.expected_return, tax_drag=asset.tax_drag, volatility=asset.volatility, return_volatility=asset.return_volatility))
        return assets_copy

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
            assets_copy = WealthService.create_asset_copy(assets)
            paths.append(self.simulate_path(assets_copy, asset_rule_map, years))
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
        peak = sum([asset.initial_value for asset in assets])
        portfolio_total = peak
        max_drawdown = 0.0
        rng = np.random.default_rng()
        no_growth_total = peak
        isLoss = False
        original_returns = [asset.expected_return for asset in assets]
        # Simulate monthly growth
        for i in range(years * 12):
            for i in range(len(assets)):
                asset_total = self.simulate_asset_growth(assets[i], asset_rule_map[assets[i].name], original_returns[i], rng)
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
    
    def simulate_asset_growth(self, asset, rules, mean_rate, rng: np.random.Generator):
        dt = 1.0 / 12.0
        asset_total = asset.initial_value
        rate = asset.expected_return
        z = rng.normal(0, 1)
        # Simulating stochastic rate change
        rate_change =  (mean_rate - rate) * dt + asset.return_volatility * np.sqrt(dt) * rng.normal(0,1) 
        rate += rate_change
        rate = max(rate, 0.0)
        asset.expected_return = rate
        # Simulating monte-carlo asset growth
        growth = np.exp((rate - 0.5 * asset.volatility ** 2) * dt + asset.volatility * np.sqrt(dt) * z)
        new_value = asset_total * growth
        gain = new_value - asset_total
        if gain > 0:
            gain = gain * (1 - asset.tax_drag) 
        asset_total = asset_total + gain + sum([rule.rate for rule in rules])
        asset.initial_value = asset_total
        return gain




        

