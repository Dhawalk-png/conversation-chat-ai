import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.chat_engine import ChatEngine
from backend.models import ChatRequest, ChatResponse, HealthResponse
from config.settings import settings
import uvicorn
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#INITIALIZE APP
app = FastAPI(title = settings.API_TITLE, version = settings.API_VERSION, description = settings.API_DESCRIPTION) 

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"]
)

#initialsie chatengine
try: 
    chat_engine = ChatEngine()
except ValueError as e:
    print(f"error initailaizing chat engine: {str(e)}")
    chat_engine =None



@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint to verify backend is running."""
    if chat_engine is None:
        return HealthResponse(status="error", message="chatengine failed to initialize. check server logs for details.")
    return HealthResponse(status="ok", message="backend is healthy and chat engine is initialized.")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """endpoint to handle chat response"""
    if chat_engine is None:
        raise HTTPException(status_code=500, detail="chat engine not available. check server logs for details.")
    try:
        assistant_message = chat_engine.chat(
            user_message=request.message,
            temperature=request.temperature,
            model=request.model
        )
        return ChatResponse(
            user_message=request.message,
            assistant_message=assistant_message,
            model=request.model
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.post("/clear-chat")
async def clear_chat_history():
    """endpoint to clear chat history"""
    if chat_engine is None:
        raise HTTPException(status_code=500, detail="chatengine not available. check server logs for details.")
    chat_engine.conversation_history = []
    return {"message": "chat history cleared successfully."}

@app.get("/models")
async def get_available_models(): 
    """endpoint to get available models from chat engine"""
    if chat_engine is None:
        raise HTTPException(status_code = 500, detail = "chat engine not available. check server logs for details.")
    # For simplicity, we return a static list of models. In a real implementation, you might query the OpenAI API for available models.
    return {'models': ["gpt-3.5-turbo", "gpt-4"], "default model": "gpt-3.5-turbo"}

     

if __name__=="__main__":
    uvicorn.run("backend.main:app", host=settings.host, port=settings.port, reload=settings.reload)