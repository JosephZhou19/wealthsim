import json

from openai import OpenAI
from app.schema.AssetBase import AssetBase
from app.models.Asset import Asset
from app.schema.ContributionRuleBase import ContributionRuleBase
from app.service.assets.AIPrompts import SYSTEM_PROMPT, USER_PROMPT

class AIService:
    def build_analysis_payload(assets: list[Asset], rules, simulation_result):
        asset_jsons = [AssetBase.model_validate(asset).model_dump() for asset in assets]
        rule_jsons = [ContributionRuleBase.model_validate(rule).model_dump() for rule in rules]
        return {
            "time_horizon_years": simulation_result["years"],
            "assets": asset_jsons,
            "monthly_contributions": rule_jsons,
            "final_results": simulation_result
        }
    def generate_ai_analysis(payload):
        client = OpenAI()
        content = USER_PROMPT + json.dumps(payload, indent=2)
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0.2,  # IMPORTANT: low randomness
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": f"Simulation data:\n{content}"
                }
            ]
        )

        return response.choices[0].message.content

