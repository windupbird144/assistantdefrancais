import discord
from discord import app_commands

from assistant.llm import get_definition
from assistant.config import Config

from opentelemetry import trace

from assistant.telemetry import setup_telemetry

tracer = trace.get_tracer(__name__)

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)  # Slash command handler

    async def setup_hook(self):
        setup_telemetry()

        # Sync commands to a specific guild (faster testing)
        with tracer.start_as_current_span("setup_hook"):
            guild = discord.Object(Config.DISCORD_GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            try:
                synced = await self.tree.sync(guild=guild)
                print(
                    f"Synced {len(synced)} command(s) to guild {Config.DISCORD_GUILD_ID}"
                )
            except discord.HTTPException as e:
                print(f"Failed to sync commands: {e}")


bot = MyClient()


@bot.tree.command(name="definir", description="Obtenir la définition d'un mot")
async def definir(interaction: discord.Interaction, mot: str):
    with tracer.start_as_current_span("definir") as span:
        span.set_attribute("word", mot)
        span.set_attribute("guild_id", interaction.guild_id or "")
        span.set_attribute("user_id", interaction.user.id)
        try:
            await interaction.response.defer(thinking=True)
        except Exception:
            await interaction.followup.send(
                "Une erreur s'est produite lors du démarrage du traitement.",
                ephemeral=True,
            )
        definition = await get_definition(mot)
        await interaction.followup.send(definition)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


if __name__ == "__main__":
    bot.run(Config.DISCORD_TOKEN)
