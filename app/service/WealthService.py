from app.database.database import SessionLocal
from app.crud import AssetCrud, ContributionRuleCrud, SimulationCrud
from app.models.Asset import Asset
from app.schema.SimulationRunBase import SimulationRunBase
from app.schema.SimulationResultBase import SimulationResultBase
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
    
    @staticmethod
    def calculate_pear_year_percentiles(path_data):
        yearly_results = []
        for i in range(len(path_data[0][0])):
            percentiles = dict()
            totals_for_year = [path[0][i] for path in path_data]
            percentiles["p5"] = np.percentile(totals_for_year, 5)
            percentiles["p25"] = np.percentile(totals_for_year, 25)
            percentiles["p50"] = np.percentile(totals_for_year, 50)
            percentiles["p75"] = np.percentile(totals_for_year, 75)
            percentiles["p95"] = np.percentile(totals_for_year, 95)
            yearly_results.append(percentiles)
        return yearly_results
    
    def simulate_advanced_wealth(self, years: int, seed: int | None):
        db = SessionLocal()
        assets = AssetCrud.get_assets(db)
        rules = ContributionRuleCrud.get_rules(db)
        if not assets:
            return {"error": "No assets found"}
        asset_rule_map = {}
        for asset in assets:
            asset_rule_map[asset.name] = []
            for rule in rules:
                if asset.name == rule.asset_name:
                    asset_rule_map[asset.name].append(rule)
        paths = []
        if seed is None:
            seed = np.random.SeedSequence().entropy
        rng = np.random.default_rng(seed)
        for i in range(self.MT_PATHS):
            assets_copy = WealthService.create_asset_copy(assets)
            paths.append(self.simulate_path(assets_copy, asset_rule_map, years, rng))
        wealth_totals = [path[0][-1] for path in paths]
        # returns year by year data for graphing
        per_year_percentiles = WealthService.calculate_pear_year_percentiles(paths)
        p25 = per_year_percentiles[-1]["p25"]
        p75 = per_year_percentiles[-1]["p75"]
        p50 = per_year_percentiles[-1]["p50"]
        p5 = per_year_percentiles[-1]["p5"]
        p95 = per_year_percentiles[-1]["p95"]
        max_drawdown = max([path[1] for path in paths])
        probability_of_loss = sum([path[2] for path in paths]) / len(paths)
        metrics={}
        simulation_run = SimulationRunBase(period=years, seed=str(seed), num_simulations=self.MT_PATHS)
        simulation_run = SimulationCrud.createSimulationRun(db, simulationRun=simulation_run)
        simulation_result = SimulationResultBase(run_id=simulation_run.id,final_value_p50=p50, final_value_p25=p25, final_value_p75=p75, final_value_p5=p5, final_value_p95=p95, max_drawdown=max_drawdown, probability_of_loss=probability_of_loss, metrics=metrics)
        SimulationCrud.createSimulationResult(db, simulationResult=simulation_result)
        db.close()
        return {
            "final_result": {
                "p5": p5,
                "p25": p25,
                "p50": p50,
                "p75": p75,
                "p95": p95,
                "max_drawdown": max_drawdown,
                "probability_of_loss": probability_of_loss,
                "seed": str(seed)
            },
            "yearly_timeline" : per_year_percentiles
        }
    
    def simulate_path(self, assets, asset_rule_map, years, rng: np.random.Generator):
        per_year_data = []
        peak = sum([asset.initial_value for asset in assets])
        portfolio_total = peak
        max_drawdown = 0.0
        no_growth_total = peak
        isLoss = False
        original_returns = [asset.expected_return for asset in assets]
        # Simulate monthly growth
        for i in range(years * 12):
            if i % 12 == 0:
                per_year_data.append(portfolio_total)
            for i in range(len(assets)):
                self.simulate_asset_rate_change(assets[i], original_returns[i], rng)
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
        return per_year_data, max_dd, isLoss
    
    def simulate_asset_rate_change(self, asset, mean_rate, rng: np.random.Generator):
        dt = 1.0 / 12.0
        rate = asset.expected_return
        # Simulating stochastic rate change
        rate_change =  (mean_rate - rate) * dt + asset.return_volatility * np.sqrt(dt) * rng.normal(0,1) 
        rate += rate_change
        rate = max(rate, 0.0)
        asset.expected_return = rate

    def simulate_asset_growth(self, asset, rules, mean_rate, rng: np.random.Generator):
        dt = 1.0 / 12.0
        asset_total = asset.initial_value
        rate = asset.expected_return
        z = rng.normal(0, 1)
        # Simulating monte-carlo asset growth
        growth = np.exp((rate - 0.5 * asset.volatility ** 2) * dt + asset.volatility * np.sqrt(dt) * z)
        new_value = asset_total * growth
        gain = new_value - asset_total
        if gain > 0:
            gain = gain * (1 - asset.tax_drag) 
        asset_total = asset_total + gain + sum([rule.rate for rule in rules])
        asset.initial_value = asset_total
        return gain




        

