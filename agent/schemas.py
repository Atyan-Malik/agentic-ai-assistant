
from typing import Literal

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class AgentRequest(BaseModel):
    message: str = Field(..., min_length=1)
    session_id: str | None = None


class AgentResponse(BaseModel):
    response: str
    session_id: str
    model: str = "qwen2.5:latest"
    success: bool = True
    error: str | None = None
