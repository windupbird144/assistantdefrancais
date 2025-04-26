# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    OPENROUTER_API_KEY: str = os.environ["OPENROUTER_API_KEY"]
    OPENROUTER_API_URL: str = os.environ["OPENROUTER_API_URL"]
    DISCORD_TOKEN: str = os.environ["DISCORD_TOKEN"]
    DISCORD_GUILD_ID: int = int(os.environ["DISCORD_GUILD_ID"])
    foo = os.environ[""]
