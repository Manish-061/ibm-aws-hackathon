import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "").strip()
    BEDROCK_KB_ID = os.getenv("BEDROCK_KB_ID", "").strip()
    
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")

settings = Settings()
