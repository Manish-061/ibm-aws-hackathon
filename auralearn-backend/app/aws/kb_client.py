from app.aws.bedrock_client import BedrockClient


class KnowledgeBaseClient:
    def __init__(self):
        self.bedrock = BedrockClient()

    def search(self, query: str):
        print(f"[KB Search] Query: {query}")
        results = self.bedrock.retrieve_from_kb(query)
        print(f"[KB Search] Retrieved {len(results)} raw results.")

        documents = []
        for item in results:
            documents.append({
                "content": item.get("content", {}).get("text", ""),
                "score": item.get("score", 0.0),
                "source": item.get("location", {})
            })

        return documents
