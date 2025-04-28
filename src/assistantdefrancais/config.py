import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path.cwd() / '.env.default')
load_dotenv(Path.cwd() / '.env')

class Config:
    DISCORD_TOKEN: str = os.environ["DISCORD_TOKEN"]
    OPENROUTER_API_KEY: str = os.environ["OPENROUTER_API_KEY"]
    OPENROUTER_MODEL: str = os.environ["OPENROUTER_MODEL"]
    OPENROUTER_API_URL: str = os.environ["OPENROUTER_API_URL"]
    DISCORD_GUILD_ID: int | None = int(guild_id) if (guild_id := os.getenv("DISCORD_GUILD_ID")) else None
    OPENROUTER_GENERATION_API_URL: str = os.environ['OPENROUTER_GENERATION_API_URL']