import os
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()


class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)  # Slash command handler

    async def setup_hook(self):
        # Sync commands to a specific guild (faster testing)
        guild = discord.Object(id=int(os.environ["DISCORD_GUILD_ID"]))
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)


bot = MyClient()


@bot.tree.command(name="definir", description="Obtenir la définition d'un mot")
async def definir(interaction: discord.Interaction, mot: str):
    # Simulate an LLM API call (we'll replace this later)
    fake_llm_response = f"**Définition de '{mot}'**: (Exemple de réponse simulée)"

    await interaction.response.send_message(fake_llm_response)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


if __name__ == "__main__":
    bot.run(os.environ["DISCORD_TOKEN"])
