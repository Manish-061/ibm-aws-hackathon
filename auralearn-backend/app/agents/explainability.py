import json
import re
from typing import Dict, Any
from app.aws.bedrock_client import BedrockClient

class ExplainabilityAgent:
    def __init__(self):
        self.bedrock = BedrockClient()

    def run(self, goal_context: Dict[str, Any], learning_path: Dict[str, Any], cross_domain_impact: Dict[str, str]) -> Dict[str, Any]:
        """
        Generates a human-understandable explanation for the AI's decisions.
        """
        
        goal = goal_context.get("raw_input", "unknown goal")
        skills_summary = ", ".join(
            learning_path.get("foundation", []) + 
            learning_path.get("intermediate", []) + 
            learning_path.get("advanced", [])
        )
        
        prompt = f"""
        You are an AI explainability engine. Your job is to explain WHY the system generated the specific learning plan it did.
        
        User Goal: "{goal}"
        Selected Skills: {skills_summary}
        Cross-Domain Impacts: {json.dumps(cross_domain_impact)}
        
        Provide an explanation in JSON format with the following keys:
        - "summary" (string): A brief explanation of why these skills were chosen for the goal.
        - "assumptions" (list of strings): 2-3 assumptions the AI made about the user's background or intent.
        - "confidence" (string): "High", "Medium", or "Low" based on the clarity of the goal and available knowledge.
        
        Example format:
        {{
            "summary": "This plan focuses on backend technologies because your goal mentioned server-side development.",
            "assumptions": ["User knows basic coding", "User wants industry-standard tools"],
            "confidence": "High"
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
                "summary": "Generated based on top relevance matches in the Knowledge Base.",
                "assumptions": ["Standard learning progression"],
                "confidence": "Medium"
            }
