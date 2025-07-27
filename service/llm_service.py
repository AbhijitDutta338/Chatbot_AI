import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()  # Load GOOGLE_API_KEY from .env

class LLMService:
    _instance = None
    _model = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            api_key = os.getenv("GOOGLE_API_KEY")
            genai.configure(api_key=api_key)
            # Use LangChain's Google Generative AI wrapper
            cls._model = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=api_key,
                temperature=0.7
            )
        return cls._instance

    @property
    def model(self):
        return self._model
