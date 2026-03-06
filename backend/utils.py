import logging
from typing import Optional

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getlogger(name)
    handler = logging.streamhandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -  %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

class ChatEngineError(Exception):
    """Base exception for chat engine errors."""

class APIError(ChatEngineError):
    """raised when OpenAI API call fails"""
    pass