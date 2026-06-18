from typing import Optional

import httpx
from app.config import settings
from fastapi import HTTPException


class RAGService:
    """Service to interact with the external RAG router API."""

    def __init__(self):
        self.api_url = settings.RAG_API_URL
        self.api_key = settings.RAG_API_KEY

    async def get_answer(
        self,
        question: str,
        chat_history: Optional[list] = None,
        system_context: Optional[str] = None,
        session_id: Optional[str] = None,
        subject_id: Optional[str] = None,
        subject_name: Optional[str] = None,
        grade_id: Optional[str] = None,
        grade_level: Optional[int] = None,
    ) -> dict:
        """
        Call the RAG router API and pass the selected grade + subject.

        The frontend creates a chat session with subject_id + grade_id.
        ChatService loads those values from DB and sends them here.
        This service forwards them to router_server.py so the router can activate
        the correct RAG from subject button selection.
        """
        payload = {
            "query": question,
            "session_id": session_id,
            "chat_history": chat_history or [],
            "system_context": system_context,
            "subject_id": subject_id,
            "subject_name": subject_name,
            "grade_id": grade_id,
            "grade_level": grade_level,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.api_url,
                    headers={
                        "Content-Type": "application/json",
                        "X-API-Key": self.api_key,
                    },
                    json=payload,
                    timeout=180.0,
                )

                response.raise_for_status()
                data = response.json()

                return {
                    "answer": data.get("answer") or data.get("response") or str(data),
                    "figures": data.get("figures", []),
                    "book_id": data.get("book_id"),
                    "route": data.get("route"),
                    "selected_rag": data.get("selected_rag"),
                    "selected_rag_key": data.get("selected_rag_key"),
                    "routing_mode": data.get("routing_mode"),
                    "raw": data,
                }

            except httpx.TimeoutException:
                raise HTTPException(
                    status_code=504,
                    detail="RAG API request timed out",
                )

            except httpx.RequestError:
                raise HTTPException(
                    status_code=503,
                    detail="RAG server is currently offline. Please try again after some time.",
                )

            except httpx.HTTPStatusError as e:
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"RAG API error: {e.response.text}",
                )

            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error calling RAG: {str(e)}",
                )
