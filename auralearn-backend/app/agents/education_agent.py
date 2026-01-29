from typing import Dict, Any, List
import json
import re
from app.aws.kb_client import KnowledgeBaseClient
from app.aws.bedrock_client import BedrockClient


class EducationAgent:
    """
    RAG-only agent.
    Generates learning paths strictly from Knowledge Base content.
    """

    def __init__(self):
        self.kb = KnowledgeBaseClient()
        self.bedrock = BedrockClient()

    def _extract_skills(self, documents: List[Dict[str, Any]], goal: str) -> List[str]:
        """
        Uses LLM to extract specific technical skills from the retrieved documents.
        Crucially, it validates if the content is actually RELEVANT to the user's goal.
        """
        if not documents:
            return []

        # Aggregate context from top documents
        context_text = "\n\n".join([doc.get("content", "") for doc in documents[:3]])

        prompt = f"""
        You are a strict content validator and curriculum designer. 
        
        User Goal: "{goal}"
        
        Retrieved Knowledge Base Content:
        {context_text}
        
        Task:
        1. Determine if the retrieved content contains specific information relevant to the User Goal.
        2. If the content is about a completely different topic (e.g., User asks for "Java/Spring Boot" but content is only about "Python/Flask"), you MUST return the single word: IRRELEVANT.
        3. If the content IS relevant, extract the specific technical skills, concepts, and tools mentioned in the text.
        
        Return ONLY:
        - The word "IRRELEVANT" if the content does not match the goal.
        - OR a comma-separated list of skills found in the text.
        """

        response = self.bedrock.generate_text(prompt)
        
        if "IRRELEVANT" in response.upper():
            return []
        
        # Clean up response
        skills_list = [s.strip() for s in response.split(",") if s.strip()]
        return list(set(skills_list))

    def _structure_learning_path(self, skills: List[str], goal: str) -> Dict[str, Any]:
        """
        Uses LLM to organize the extracted skills into a logical learning progression based on the user's goal.
        """
        skills_str = ", ".join(skills)
        
        prompt = f"""
        You are an expert curriculum developer. 
        User Goal: "{goal}"
        Available Skills: {skills_str}
        
        Organize ONLY the provided available skills into a 3-stage learning roadmap (Foundation, Intermediate, Advanced).
        Do not add skills that were not in the provided list.
        
        Return the result as valid JSON with the keys: "foundation", "intermediate", "advanced".
        Each key should contain a list of strings.
        
        Example format:
        {{
            "foundation": ["Skill A", "Skill B"],
            "intermediate": ["Skill C"],
            "advanced": ["Skill D"]
        }}
        """

        response = self.bedrock.generate_text(prompt)
        
        # specific logic to find and parse JSON in case of chatty model output
        try:
            # simple regex to extract json block if wrapped in code blocks or text
            match = re.search(r'\{.*\}', response, re.DOTALL)
            if match:
                json_str = match.group(0)
                return json.loads(json_str)
            else:
                return json.loads(response)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "foundation": skills[:len(skills)//3],
                "intermediate": skills[len(skills)//3:2*len(skills)//3],
                "advanced": skills[2*len(skills)//3:]
            }

    def run(self, goal_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution method.
        """
        query = goal_context.get("raw_input")

        # Step 1: Retrieve grounded knowledge
        retrieved_docs = self.kb.search(query)

        if not retrieved_docs:
            return {
                "status": "insufficient_knowledge",
                "message": "Knowledge Base does not contain sufficient information for this goal.",
                "learning_path": None
            }

        # Step 2: Extract skills using LLM (with Relevance Check)
        skills = self._extract_skills(retrieved_docs, query)

        # If strict extraction returned nothing (irrelevant content), fail safely.
        if not skills:
             return {
                "status": "insufficient_knowledge",
                "message": "Sorry, I am unable to assist you with this request. Try something else while I increase my knowledge.",
                "learning_path": None
            }

        # Step 3: Structure learning stages using LLM
        learning_path = self._structure_learning_path(skills, query)

        return {
            "status": "success",
            "goal": query,
            "skills_identified": skills,
            "learning_path": learning_path,
            "source_documents": [
                {
                    "score": doc.get("score"),
                    "source": doc.get("source")
                }
                for doc in retrieved_docs
            ]
        }
