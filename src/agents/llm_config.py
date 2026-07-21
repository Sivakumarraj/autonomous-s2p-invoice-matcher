import os
from dotenv import load_dotenv
from pydantic_ai.models.gemini import GeminiModel

# Load GEMINI_API_KEY securely from .env
load_dotenv()

# By instantiating GeminiModel directly, we bypass the string validation check.
# This forces PydanticAI to use the brand new 2.5-flash model.
gemma_model = GeminiModel(
    'gemini-2.5-flash', 
    api_key=os.environ.get("GEMINI_API_KEY")
)