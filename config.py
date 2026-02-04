import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ENABLE_AI = os.getenv("ENABLE_AI", "false").lower() in ("1", "true", "yes")
DATABASE_URL = os.getenv("DATABASE_URL")

