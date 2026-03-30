import httpx
from app.config import settings
from fastapi import HTTPException

class RAGService:
    """Service to interact with your RAG API"""
    
    def __init__(self):
        self.api_url = settings.RAG_API_URL
        self.api_key = settings.RAG_API_KEY
    
    async def get_answer(self, question: str, chat_history: list = None) -> dict:
        """
        Call your RAG API to get an answer
        """
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.api_url,
                    headers={
                        "Content-Type": "application/json",
                        "X-API-Key": self.api_key
                    },
                    json={
                        "query": question,
                        "book_id": "biology_9",
                        "session_id": None
                    },
                    timeout=60.0
                )
                
                response.raise_for_status()
                data = response.json()
                
                return {
                    "answer": data.get("answer") or data.get("response") or str(data),
                    "figures": data.get("figures", [])
                }
                
            except httpx.TimeoutException:
                raise HTTPException(
                    status_code=504,
                    detail="RAG API request timed out"
                )
            except httpx.HTTPStatusError as e:
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"RAG API error: {e.response.text}"
                )
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error calling RAG: {str(e)}"
                )