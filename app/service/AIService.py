import json

from openai import OpenAI
from app.models.Profile import Profile
from app.schema.AssetBase import AssetBase
from app.models.Asset import Asset
from app.schema.ChatBase import ChatMessage
from app.schema.ContributionRuleBase import ContributionRuleBase
from app.schema.ProfileBase import ProfileBase
from app.schema.SimulationResultBase import SimulationResultBase

class AIService:
    def build_analysis_payload(assets: list[Asset], rules, simulation_run, simulation_result, profile: Profile):
        asset_jsons = [AssetBase.model_validate(asset).model_dump() for asset in assets]
        rule_jsons = [ContributionRuleBase.model_validate(rule).model_dump() for rule in rules]
        profile_jsons = ProfileBase.model_validate(profile).model_dump()
        result_jsons = SimulationResultBase.model_validate(simulation_result).model_dump()
        del result_jsons["run_id"]
        del result_jsons["metrics"]
        system_prompt = f"""
        You are a financial decision-support assistant.
        Do not give specific investment advice. 
        Analyze Monte Carlo simulation results, user profile, and asset allocation.
        The simulation was set for {simulation_run.period} years.
        USER PROFILE:
           {profile_jsons}
        Assets:
            {asset_jsons}
        Monthly Contributions:
            {rule_jsons}
        
        Simulation Results: 
            {result_jsons}
        """
        return system_prompt
    
    def generate_ai_analysis(system_prompt, messages: list[ChatMessage]):
        conversation = [{"role": "system", "content": system_prompt}]
        for message in messages:
            conversation.append({"role": message.role, "content": message.content})
        print(conversation)
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0.7,
            messages=conversation
        )

        return response.choices[0].message.content

