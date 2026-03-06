import os
from dotenv import load_dotenv
from openai import OpenAI
from config.settings import settings

# load environment .env file
load_dotenv()
class ChatEngine:
    """ChatEngine class to handle chat interactions with OpenAI API."""
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in settings. please set it in config/settings.py")
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-3.5-turbo"
        self.conversation_history = []

    def chat(self, user_message: str, temperature= 0.7, model=None):
            """
            sends a message to openAO amd returns the assistants response.
            """
            if model:
                self.model = model
            self.conversation_history.append({"role":"user", "content":user_message})

            try:
                response = self.client.chat.completions.create(
                    model = self.model,
                    messages = self.conversation_history,
                    temperature=temperature,
                    max_tokens= 500
                )
                assistant_message = response.choices[0].message.content
                self.conversation_history.append({"role":"assistant","content":assistant_message})
                return assistant_message
            except Exception as e:
                print(f" Error calling Openai API: {str(e)}")
                raise
        
    def clear_history(self):
            """Clears the conversation history."""
            self.conversation_history = []

    def get_history(self):
            """return the current conversation history"""
            return self.conversation_history