import dotenv
import logfire
from pydantic_settings import BaseSettings

dotenv.load_dotenv()

logfire.configure()
logfire.instrument_pydantic_ai()


class Settings(BaseSettings):
    LLM_API_KEY: str
    LLM_BASE_URL: str
    LLM_MODEL_NAME: str


settings = Settings()
