import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    OPENROUTER_API_KEY: str | None = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_API_URL: str | None = os.getenv("OPENROUTER_API_URL")
    DISCORD_TOKEN: str | None = os.getenv("DISCORD_TOKEN")
    DISCORD_GUILD_ID: int | None = int(os.getenv("DISCORD_GUILD_ID", "0"))
