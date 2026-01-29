import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from app.api.routes import router
import uvicorn

app = FastAPI(
    title="AURA-Learn Backend",
    description="Agentic AI backend using Amazon Bedrock",
    version="0.1.0"
)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
