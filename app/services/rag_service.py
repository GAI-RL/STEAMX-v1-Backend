import httpx
from app.config import settings
from fastapi import HTTPException

class RAGService:
    """Service to interact with your RAG API"""
    
    def __init__(self):
        self.api_url = settings.RAG_API_URL
        self.api_key = settings.RAG_API_KEY
    
    async def get_answer(self, question: str, chat_history: list = None) -> str:
        """
        Call your RAG API to get an answer
        """
        
        async with httpx.AsyncClient() as client:
            try:
                # Try different authentication methods
                
                # METHOD 1: API key in header (no Bearer)
                response = await client.post(
                    self.api_url,
                    headers={
                        "Content-Type": "application/json",
                        "X-API-Key": self.api_key  # Changed from Authorization
                    },
                    json={
                        "question": question
                    },
                    timeout=60.0
                )
                
                response.raise_for_status()
                data = response.json()
                
                # Extract answer - adjust based on your response
                answer = data.get("answer") or data.get("response") or str(data)
                
                return answer
                
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