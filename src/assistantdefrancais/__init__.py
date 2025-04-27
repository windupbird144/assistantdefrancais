from .bot import bot
from .config import Config


def main():
    bot.run(Config.DISCORD_TOKEN)
