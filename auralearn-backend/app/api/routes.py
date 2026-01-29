from fastapi import APIRouter
from app.aws.kb_client import KnowledgeBaseClient
from app.aws.bedrock_client import BedrockClient
from app.agents.orchestrator import OrchestratorAgent

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/orchestrate")
def orchestrate(user_input: str):
    orchestrator = OrchestratorAgent()
    return orchestrator.execute(user_input)

@router.get("/test-kb")
def test_kb(query: str):
    kb = KnowledgeBaseClient()
    results = kb.search(query)
    return {
        "query": query,
        "results": results
    }

@router.post("/learn")
def learn_skill(skill: str, user_level: str = "Beginner", context: str = ""):
    """
    Generate educational content for a specific skill using Amazon Bedrock LLM.
    """
    bedrock = BedrockClient()
    
    prompt = f"""
    You are an expert educator and mentor. Create a comprehensive yet concise learning module for the following skill.
    
    **Skill to Learn:** {skill}
    **Student Level:** {user_level}
    **Additional Context:** {context if context else "None provided"}
    
    Please provide:
    
    1. **Introduction** (2-3 sentences explaining what this skill is and why it matters)
    
    2. **Key Concepts** (3-5 core concepts the student must understand, with brief explanations)
    
    3. **Practical Example** (A real-world code snippet or scenario demonstrating the skill)
    
    4. **Common Mistakes** (2-3 mistakes beginners make and how to avoid them)
    
    5. **Next Steps** (What to learn after mastering this skill)
    
    Format your response in a clear, structured way that's easy to read and follow.
    Keep the total response under 800 words for optimal readability.
    """
    
    try:
        response = bedrock.generate_text(prompt)
        return {
            "status": "success",
            "skill": skill,
            "level": user_level,
            "content": response
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "skill": skill
        }

@router.post("/chat")
def chat_with_tutor(message: str, skill_context: str = "", conversation_history: str = ""):
    """
    Interactive chat with AI tutor about a specific skill or topic.
    """
    bedrock = BedrockClient()
    
    prompt = f"""
    You are AURA, an AI learning tutor. You help students understand technical concepts clearly and patiently.
    
    Current Topic/Skill Context: {skill_context if skill_context else "General programming and technology"}
    
    Previous Conversation:
    {conversation_history if conversation_history else "This is the start of the conversation."}
    
    Student's Question/Message: {message}
    
    Respond helpfully and concisely. If asked to explain something, use simple language and examples.
    If asked for code, provide working examples with comments.
    Keep responses focused and under 300 words unless a longer explanation is truly needed.
    """
    
    try:
        response = bedrock.generate_text(prompt)
        return {
            "status": "success",
            "response": response
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

