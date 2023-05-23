from discord import Interaction
from discord.app_commands import command, Group, autocomplete, Choice, describe
from discord.ext.commands import Cog, Bot
import traceback


class CustomCog(Cog):

    # group = Group(name="command", description="A group pertaining to custom commands.")

    def __init__(self, bot) -> None:
        self.client = bot

    # @group.command(name="create", description="Creates a custom command.")
    # @describe(name="Name of command", response="Command response")
    # async def create_command(self, interaction: Interaction, name: str, response: str) -> None:
    #     pass


async def setup(bot) -> None:
    await bot.add_cog(CustomCog(bot))
