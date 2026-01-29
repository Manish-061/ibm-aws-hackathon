from typing import Dict, Any, List
from app.aws.bedrock_client import BedrockClient
from app.agents.education_agent import EducationAgent
from app.agents.cross_domain_agent import CrossDomainAgent
from app.agents.explainability import ExplainabilityAgent


class OrchestratorAgent:
    """
    Central planning and coordination agent.
    Owns decision flow, not domain logic.
    """

    def __init__(self):
        self.bedrock = BedrockClient()
        self.education_agent = EducationAgent()
        self.cross_domain_agent = CrossDomainAgent()
        self.explainability_agent = ExplainabilityAgent()

    def interpret_goal(self, user_input: str) -> Dict[str, Any]:
        """
        Uses Nova Premier to interpret and structure the user's goal.
        """
        prompt = f"""
        Interpret the following user goal.
        Extract:
        - primary goal
        - constraints (time, level, focus)
        - assumptions (if any)

        User input:
        {user_input}

        Return a structured interpretation.
        """

        response = self.bedrock.generate_text(prompt)

        return {
            "raw_input": user_input,
            "interpreted_goal": response
        }

    def plan(self, interpreted_goal: Dict[str, Any]) -> List[str]:
        """
        Creates a high-level execution plan.
        """
        return [
            "generate_learning_path",
            "map_cross_domain_impact",
            "generate_explanation"
        ]

    def execute(self, user_input: str) -> Dict[str, Any]:
        """
        Full orchestration pipeline.
        """
        decision_trace = {}

        # Step 1: Interpret goal
        goal_context = self.interpret_goal(user_input)
        decision_trace["goal_interpretation"] = goal_context

        # Step 2: Plan
        plan_steps = self.plan(goal_context)
        decision_trace["plan"] = plan_steps

        # Step 3: Execute Education Agent
        learning_path = self.education_agent.run(goal_context)
        decision_trace["education_output"] = learning_path

        # Step 4: Execute Cross-Domain Agent
        cross_domain_impact = self.cross_domain_agent.run(learning_path)
        decision_trace["cross_domain_output"] = cross_domain_impact

        # Step 5: Explainability
        explanation = self.explainability_agent.run(
            goal_context=goal_context,
            learning_path=learning_path,
            cross_domain_impact=cross_domain_impact
        )

        decision_trace["explanation"] = explanation

        return {
            "learning_plan": learning_path,
            "cross_domain_impact": cross_domain_impact,
            "explanation": explanation,
            "decision_trace": decision_trace
        }
