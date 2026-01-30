import json
import re
from typing import Dict, Any, List
from app.aws.bedrock_client import BedrockClient
from app.aws.kb_client import KnowledgeBaseClient


class CrossDomainAgent:
    """
    Agent that maps educational skills to cross-domain applications
    using grounded knowledge from the Bedrock Knowledge Base.
    """
    
    def __init__(self):
        self.bedrock = BedrockClient()
        self.kb = KnowledgeBaseClient()
        
        # Domain-specific search queries to retrieve from KB
        self.domain_queries = {
            "health": "education to health healthcare medical applications skills transfer",
            "finance": "education to finance financial banking applications skills transfer",
            "agriculture": "education to agriculture farming crop applications skills transfer"
        }
    
    def _retrieve_domain_context(self, domain: str, skills: List[str]) -> str:
        """
        Retrieves relevant context from the Knowledge Base for a specific domain.
        """
        skills_str = " ".join(skills[:5])  # Use top 5 skills for context
        query = f"{self.domain_queries.get(domain, domain)} {skills_str}"
        
        print(f"[CrossDomain] Searching KB for domain '{domain}' with query: {query[:100]}...")
        
        documents = self.kb.search(query)
        
        if not documents:
            print(f"[CrossDomain] No documents found for domain '{domain}'")
            return ""
        
        # Combine top 3 document contents
        context_parts = []
        for doc in documents[:3]:
            content = doc.get("content", "")
            if content:
                context_parts.append(content)
                print(f"[CrossDomain] Found content for '{domain}' (score: {doc.get('score', 'N/A')})")
        
        return "\n\n".join(context_parts)
    
    def _generate_domain_application(self, domain: str, skills: List[str], kb_context: str) -> str:
        """
        Generates domain-specific skill application using LLM grounded in KB content.
        """
        skills_summary = ", ".join(skills)
        
        if kb_context:
            # Use KB-grounded prompt
            prompt = f"""
            You are a cross-domain career analyst. Your task is to explain how educational skills 
            can be applied to the {domain.upper()} domain.
            
            USER'S SKILLS:
            {skills_summary}
            
            KNOWLEDGE BASE REFERENCE (Use this as your primary source):
            {kb_context}
            
            Based ONLY on the knowledge base content above, provide a specific, concise explanation 
            (2-3 sentences max) of how these skills apply to {domain}. 
            
            Focus on concrete applications mentioned in the knowledge base.
            Do NOT make up information. If the knowledge base doesn't mention something, don't include it.
            """
        else:
            # Fallback if no KB content - be conservative
            prompt = f"""
            You are a cross-domain career analyst.
            
            Skills: {skills_summary}
            
            Provide a brief, general statement (1 sentence) about how these technical skills 
            might be relevant to the {domain} domain. Be conservative and factual.
            """
        
        response = self.bedrock.generate_text(prompt)
        
        # Clean up the response - extract just the core content
        response = response.strip()
        # Remove any markdown or extra formatting
        response = re.sub(r'^[\s\S]*?(?=[A-Z])', '', response, count=1) if response else response
        
        return response if response else f"Skills can be applied to {domain} sector."
    
    def run(self, learning_path: Dict[str, Any]) -> Dict[str, str]:
        """
        Determines how the generated learning path can be applied to other domains.
        Uses Knowledge Base retrieval for grounded, factual responses.
        """
        # Extract all skills from the learning path
        all_skills = (
            learning_path.get("foundation", []) + 
            learning_path.get("intermediate", []) + 
            learning_path.get("advanced", [])
        )
        
        if not all_skills:
            # Fallback if learning path has no skills
            all_skills = learning_path.get("skills_identified", ["general technical skills"])
        
        print(f"[CrossDomain] Processing {len(all_skills)} skills for cross-domain mapping...")
        
        results = {}
        
        # Process each domain
        for domain in ["health", "finance", "agriculture"]:
            print(f"[CrossDomain] Processing domain: {domain}")
            
            # Step 1: Retrieve relevant KB content for this domain
            kb_context = self._retrieve_domain_context(domain, all_skills)
            
            # Step 2: Generate domain-specific application grounded in KB
            application = self._generate_domain_application(domain, all_skills, kb_context)
            
            results[domain] = application
        
        print(f"[CrossDomain] Completed. Results: {list(results.keys())}")
        
        return results
