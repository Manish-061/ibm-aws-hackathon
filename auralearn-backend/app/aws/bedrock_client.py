import boto3
import json
from app.core.config import settings


class BedrockClient:
    def __init__(self):
        # Prepare session args if credentials are provided explicitly in .env
        session_kwargs = {
            "region_name": settings.AWS_REGION
        }
        
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            session_kwargs["aws_access_key_id"] = settings.AWS_ACCESS_KEY_ID
            session_kwargs["aws_secret_access_key"] = settings.AWS_SECRET_ACCESS_KEY
            if settings.AWS_SESSION_TOKEN:
                session_kwargs["aws_session_token"] = settings.AWS_SESSION_TOKEN

        self.runtime = boto3.client(
            service_name="bedrock-runtime",
            **session_kwargs
        )

        self.agent_runtime = boto3.client(
            service_name="bedrock-agent-runtime",
            **session_kwargs
        )

    def generate_text(self, prompt: str) -> str:
        """
        Calls Nova Premier (or Claude/Titan) for orchestration / reasoning.
        """
        # Method 1: Use the Converse API (Preferred for Nova/Claude)
        try:
            response = self.runtime.converse(
                modelId=settings.BEDROCK_MODEL_ID,
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": prompt}]
                    }
                ],
                inferenceConfig={
                    "maxTokens": 1024,
                    "temperature": 0.2
                }
            )
            return response["output"]["message"]["content"][0]["text"]
            
        except (AttributeError, Exception) as e:
            # Fallback for older boto3 or if converse fails for other reasons
            # Proceed to invoke_model with manual payload
            print(f"Converse API attempt failed ({e}), falling back to invoke_model.")
            pass

        # Method 2: Manual invoke_model (Payload customized for Nova/Claude)
        body = {
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ],
            "inferenceConfig": {
                "temperature": 0.2,
                "max_new_tokens": 1024  # Nova uses max_new_tokens, not maxTokens
            }
        }

        try:
            response = self.runtime.invoke_model(
                modelId=settings.BEDROCK_MODEL_ID,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(body)
            )
            
            response_body = json.loads(response.get("body").read())
            
            # Nova / Claude 3 (Messages API)
            if "output" in response_body:
                 return response_body["output"]["message"]["content"][0]["text"]
            
            # Claude 3 direct
            if "content" in response_body and isinstance(response_body["content"], list):
                return response_body["content"][0]["text"]
                
             # Titan / Legacy
            if "results" in response_body:
                return response_body["results"][0]["outputText"]
                
            return str(response_body)

        except Exception as e:
            print(f"Error invoking Bedrock: {e}")
            return "Error generating response. Please check AWS configuration."

    def retrieve_from_kb(self, query: str, top_k: int = 5):
        """
        Retrieves grounded documents from Bedrock Knowledge Base.
        """
        response = self.agent_runtime.retrieve(
            knowledgeBaseId=settings.BEDROCK_KB_ID,
            retrievalQuery={
                "text": query
            },
            retrievalConfiguration={
                "vectorSearchConfiguration": {
                    "numberOfResults": top_k
                }
            }
        )

        return response.get("retrievalResults", [])
