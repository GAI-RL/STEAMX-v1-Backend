from pydantic import BaseModel

class FeedbackCreate(BaseModel):
    rating: int  # 1-5
    comment: str | None = None

class FeedbackResponse(BaseModel):
    message: str