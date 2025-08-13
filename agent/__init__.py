from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from settings import settings

chat_llm = OpenAIModel(model_name=settings.LLM_MODEL_NAME, provider=OpenAIProvider(
    base_url=settings.LLM_BASE_URL, api_key=settings.LLM_API_KEY,
))
