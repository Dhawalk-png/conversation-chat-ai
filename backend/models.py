from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    model: str
    temperature: float

class ChatResponse(BaseModel):
    user_message: str
    assistant_message: str
    model: str

class HealthResponse(BaseModel):
    status: str
    message: str

