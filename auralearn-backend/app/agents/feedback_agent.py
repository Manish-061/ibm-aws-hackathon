import json
import re
from typing import Dict, Any, List
from app.aws.bedrock_client import BedrockClient
from app.aws.kb_client import KnowledgeBaseClient


class FeedbackAgent:
    """
    Agent that processes user feedback and refines learning paths.
    Implements the feedback loop for continuous path improvement.
    """
    
    def __init__(self):
        self.bedrock = BedrockClient()
        self.kb = KnowledgeBaseClient()
    
    def _categorize_feedback(self, feedback: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Categorizes user feedback into actionable categories.
        """
        categorized = {
            "already_known": [],      # Skills user already knows
            "too_advanced": [],       # Skills too difficult right now
            "not_relevant": [],       # Skills not relevant to goal
            "want_more": [],          # Topics user wants to explore more
            "general_feedback": ""    # Free-text feedback
        }
        
        # Process skill-level feedback
        skill_feedback = feedback.get("skill_feedback", {})
        for skill, rating in skill_feedback.items():
            if rating == "already_known":
                categorized["already_known"].append(skill)
            elif rating == "too_advanced":
                categorized["too_advanced"].append(skill)
            elif rating == "not_relevant":
                categorized["not_relevant"].append(skill)
            elif rating == "want_more":
                categorized["want_more"].append(skill)
        
        categorized["general_feedback"] = feedback.get("general_feedback", "")
        
        return categorized
    
    def _retrieve_additional_content(self, topics: List[str], original_goal: str) -> str:
        """
        Retrieves additional content from KB for topics user wants to explore more.
        """
        if not topics:
            return ""
        
        query = f"{original_goal} {' '.join(topics)} advanced techniques best practices"
        print(f"[FeedbackAgent] Retrieving additional content for: {query[:100]}...")
        
        documents = self.kb.search(query)
        
        if not documents:
            return ""
        
        context_parts = []
        for doc in documents[:3]:
            content = doc.get("content", "")
            if content:
                context_parts.append(content)
        
        return "\n\n".join(context_parts)
    
    def run(
        self, 
        original_path: Dict[str, Any], 
        feedback: Dict[str, Any],
        original_goal: str
    ) -> Dict[str, Any]:
        """
        Refines the learning path based on user feedback.
        
        Args:
            original_path: The original learning path structure
            feedback: User feedback with skill ratings and comments
            original_goal: The original user goal
            
        Returns:
            Refined learning path with explanation of changes
        """
        print(f"[FeedbackAgent] Processing feedback for goal: {original_goal[:50]}...")
        
        # Step 1: Categorize the feedback
        categorized = self._categorize_feedback(feedback)
        
        print(f"[FeedbackAgent] Feedback categories:")
        print(f"  - Already known: {len(categorized['already_known'])} skills")
        print(f"  - Too advanced: {len(categorized['too_advanced'])} skills")
        print(f"  - Not relevant: {len(categorized['not_relevant'])} skills")
        print(f"  - Want more: {len(categorized['want_more'])} skills")
        
        # Step 2: Get additional KB content if user wants to explore more topics
        additional_context = ""
        if categorized["want_more"]:
            additional_context = self._retrieve_additional_content(
                categorized["want_more"], 
                original_goal
            )
        
        # Step 3: Build refinement prompt
        current_foundation = original_path.get("learning_path", {}).get("foundation", [])
        current_intermediate = original_path.get("learning_path", {}).get("intermediate", [])
        current_advanced = original_path.get("learning_path", {}).get("advanced", [])
        
        prompt = f"""
        You are an adaptive learning path designer. The user has provided feedback on their learning path.
        Your task is to refine the path based on their feedback while maintaining logical skill progression.
        
        ORIGINAL GOAL: {original_goal}
        
        CURRENT LEARNING PATH:
        - Foundation: {json.dumps(current_foundation)}
        - Intermediate: {json.dumps(current_intermediate)}
        - Advanced: {json.dumps(current_advanced)}
        
        USER FEEDBACK:
        - Skills already known (REMOVE from path): {json.dumps(categorized['already_known'])}
        - Skills too advanced (MOVE to later stage or add prerequisites): {json.dumps(categorized['too_advanced'])}
        - Skills not relevant (REMOVE from path): {json.dumps(categorized['not_relevant'])}
        - Topics to explore more (ADD related skills): {json.dumps(categorized['want_more'])}
        - General feedback: {categorized['general_feedback']}
        
        {"ADDITIONAL KNOWLEDGE BASE CONTENT (use to add new relevant skills):" + additional_context if additional_context else ""}
        
        REFINEMENT RULES:
        1. Remove skills marked as "already_known" completely
        2. For "too_advanced" skills, either move them to a later stage or add prerequisite skills before them
        3. Remove "not_relevant" skills completely
        4. For "want_more" topics, add 1-2 related advanced skills from the knowledge base content
        5. Maintain logical progression (basics before advanced)
        6. Keep the path focused and not too long (max 5-6 skills per stage)
        
        Return the result as valid JSON with the following structure:
        {{
            "foundation": ["skill1", "skill2", ...],
            "intermediate": ["skill3", "skill4", ...],
            "advanced": ["skill5", "skill6", ...],
            "changes_made": [
                "Removed X because user already knows it",
                "Added Y for deeper exploration of Z",
                ...
            ]
        }}
        """
        
        response = self.bedrock.generate_text(prompt)
        
        # Step 4: Parse the response
        try:
            match = re.search(r'\{.*\}', response, re.DOTALL)
            if match:
                json_str = match.group(0)
                refined_path = json.loads(json_str)
            else:
                refined_path = json.loads(response)
            
            # Extract changes for transparency
            changes_made = refined_path.pop("changes_made", [])
            
            return {
                "status": "success",
                "refined_path": refined_path,
                "changes_made": changes_made,
                "feedback_processed": {
                    "skills_removed": len(categorized["already_known"]) + len(categorized["not_relevant"]),
                    "skills_adjusted": len(categorized["too_advanced"]),
                    "topics_expanded": len(categorized["want_more"])
                }
            }
            
        except json.JSONDecodeError as e:
            print(f"[FeedbackAgent] JSON parsing error: {e}")
            # Fallback: Apply simple removals
            refined_foundation = [s for s in current_foundation 
                                  if s not in categorized["already_known"] 
                                  and s not in categorized["not_relevant"]]
            refined_intermediate = [s for s in current_intermediate 
                                    if s not in categorized["already_known"] 
                                    and s not in categorized["not_relevant"]]
            refined_advanced = [s for s in current_advanced 
                               if s not in categorized["already_known"] 
                               and s not in categorized["not_relevant"]]
            
            # Move too_advanced from earlier stages to advanced
            for skill in categorized["too_advanced"]:
                if skill in refined_foundation:
                    refined_foundation.remove(skill)
                    refined_intermediate.append(skill)
                elif skill in refined_intermediate:
                    refined_intermediate.remove(skill)
                    refined_advanced.append(skill)
            
            return {
                "status": "success",
                "refined_path": {
                    "foundation": refined_foundation,
                    "intermediate": refined_intermediate,
                    "advanced": refined_advanced
                },
                "changes_made": [
                    f"Removed {len(categorized['already_known'])} skills you already know",
                    f"Removed {len(categorized['not_relevant'])} irrelevant skills",
                    f"Adjusted {len(categorized['too_advanced'])} skills that were too advanced"
                ],
                "feedback_processed": {
                    "skills_removed": len(categorized["already_known"]) + len(categorized["not_relevant"]),
                    "skills_adjusted": len(categorized["too_advanced"]),
                    "topics_expanded": 0
                }
            }
