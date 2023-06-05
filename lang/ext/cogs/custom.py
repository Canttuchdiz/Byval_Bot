import asyncio
from discord import Interaction, Message, Embed, Color, AllowedMentions
from discord.app_commands import command, Group, autocomplete, Choice, describe
from discord.ext.commands import Cog, Bot
from lang.ext.models.prisma_ext import PrismaExt
from lang.ext.models.command_mdl import CommandManager, Command, CommandMentionException, UniqueException
from prisma.errors import UniqueViolationError
from typing import List
import traceback


class CustomCog(Cog):
    group = Group(name="command", description="A group pertaining to custom commands.")

    def __init__(self, bot) -> None:
        self.client = bot
        self.prisma: PrismaExt = PrismaExt()
        self.command_manager: CommandManager = CommandManager(self.client, self.prisma)
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.prisma.connect())

    async def command_autocomplete(self, interaction: Interaction, current: str) -> List[Choice]:
        commands = await self.command_manager.get_commands(interaction.guild_id)
        return [Choice(name=command_obj.name, value=command_obj.name)
                for command_obj in commands if current.lower() in command_obj.name.lower()]

    @group.command(name="create", description="Creates a custom command.")
    @describe(name="Name of command", response="Command response")
    async def create_command(self, interaction: Interaction, name: str, response: str) -> None:
        if len(name.split()) == 1:
            command_obj = Command(interaction.user.id, name.lower(), response, interaction.guild_id)
            try:
                await self.command_manager.create_command(command_obj)
                await interaction.response.send_message("Command injection successful.", ephemeral=True)
                return
            # except CommandMentionException: await interaction.response.send_message("You cannot mention any roles
            # in your command.", ephemeral=True) return
            except UniqueException:
                await interaction.response.send_message("Command with name already exists.", ephemeral=True)
                return
        await interaction.response.send_message("Command name must be one word.", ephemeral=True)

    @group.command(name="remove", description="Removes a custom command.")
    @describe(name="Name of command")
    @autocomplete(name=command_autocomplete)
    async def remove_command(self, interaction: Interaction, name: str) -> None:
        try:
            command_obj = await self.command_manager.get_command(name, interaction.guild_id)
            await self.command_manager.remove_command(command_obj)
            await interaction.response.send_message("Command deletion successful.", ephemeral=True)
        except IndexError as e:
            await interaction.response.send_message("Command does not exist.", ephemeral=True)

    @group.command(name="list", description="Lists created commands.")
    async def list_commands(self, interaction: Interaction) -> None:
        embed = await self.command_manager.commands_embed(interaction.guild_id)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        if not message.author.bot and message.content.startswith('?'):
            try:
                command_trigger = Command.parse_trigger(message.content.lower())
                response = await self.command_manager.retrieve_response(command_trigger, message.guild.id)
                if response:
                    await message.channel.send(response, allowed_mentions=AllowedMentions.none())
            except IndexError as e:
                pass


async def setup(bot) -> None:
    await bot.add_cog(CustomCog(bot))
