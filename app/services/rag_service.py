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
        payload = {
            "query": question,
            "session_id": None
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.api_url,
                    headers={
                        "Content-Type": "application/json",
                        "X-API-Key": self.api_key
                    },
                    json=payload,
                    timeout=60.0
                )

                response.raise_for_status()
                data = response.json()

                return {
                    "answer": data.get("answer") or data.get("response") or str(data),
                    "figures": data.get("figures", []),
                    "book_id": data.get("book_id"),
                    "route": data.get("route")
                }

            # ✅ Server OFFLINE / connection issue
            except httpx.RequestError:
                raise HTTPException(
                    status_code=503,
                    detail="RAG server is currently offline. Please try again after some time."
                )

            # ✅ Timeout
            except httpx.TimeoutException:
                raise HTTPException(
                    status_code=504,
                    detail="RAG API request timed out"
                )

            # ✅ API returned error
            except httpx.HTTPStatusError as e:
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"RAG API error: {e.response.text}"
                )

            # ✅ Any other unexpected error
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error calling RAG: {str(e)}"
                )