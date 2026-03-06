class Settings:
    # OpenAI configuration
    
    DEFAULT_MODEL = "gpt-3.5-turbo"
    DEFAULT_TEMPERATURE = 0.7
    MAX_TOKENS = 500

    # FastAPI configuration
    API_TITLE = "Chat Engine API"
    API_VERSION = "1.0"
    API_DESCRIPTION = "A simple chat engine api build with FASTAPI and OPENAI"

    # Conversation limits
    max_history_length = 100
    max_history_token = 10000

    # API Server config
    host = "127.0.0.1"
    port = 8000
    reload = True
    allowed_origins = ["http://localhost:8501", "http://localhost:8000", "http://127.0.0.1:8501", "http://127.0.0.1:8000"]

    # Timeout configuration (in seconds)
    REQUEST_TIMEOUT = 200
    API_TIMEOUT = 200

settings = Settings()
