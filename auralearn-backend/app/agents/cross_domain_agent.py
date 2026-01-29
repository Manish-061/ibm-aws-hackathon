import json
import re
from typing import Dict, Any
from app.aws.bedrock_client import BedrockClient

class CrossDomainAgent:
    def __init__(self):
        self.bedrock = BedrockClient()

    def run(self, learning_path: Dict[str, Any]) -> Dict[str, str]:
        """
        Determines how the generated learning path can be applied to other domains.
        """
        # Simplify learning path for the prompt
        skills_summary = ", ".join(
            learning_path.get("foundation", []) + 
            learning_path.get("intermediate", []) + 
            learning_path.get("advanced", [])
        )

        prompt = f"""
        You are a cross-domain career analyst.
        Analyze the following set of technical skills: {skills_summary}
        
        Explain how these specific skills can be applied to improve outcomes in:
        1. Healthcare
        2. Personal Finance
        3. Agriculture
        
        Return the result as valid JSON with keys: "health", "finance", "agriculture".
        Each value should be a single, concise sentence explaining the impact.
        
        Example format:
        {{
            "health": "Data analysis skills help in tracking patient outcomes.",
            "finance": "Algorithm knowledge aids in automated trading strategies.",
            "agriculture": "IoT understanding improves crop monitoring."
        }}
        """

        response = self.bedrock.generate_text(prompt)

        try:
            match = re.search(r'\{.*\}', response, re.DOTALL)
            if match:
                json_str = match.group(0)
                return json.loads(json_str)
            else:
                return json.loads(response)
        except json.JSONDecodeError:
            return {
                "health": "Skills applicable to health data analysis.",
                "finance": "Skills useful for financial modeling.",
                "agriculture": "Skills relevant to precision agriculture."
            }
