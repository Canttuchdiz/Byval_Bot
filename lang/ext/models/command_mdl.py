from __future__ import annotations
from discord import Embed, Color, Message
from discord.ext.commands import Bot
from discord.types.snowflake import Snowflake
from lang.ext.models.prisma_ext import PrismaExt
from lang.utils.constants import _RegexExp
from lang.utils.errors import UniqueException, RoleMentionException
from prisma.models import Command_MDL
from prisma.errors import UniqueViolationError
from dataclasses import dataclass
from typing import List, Union
from re import match
from enum import Enum
import inspect


# class Status(Enum):
#     SUCCESS = 0
#     INVALID_ROLE = 1
#     UNIQUE_VIOLATION = 2


@dataclass
class Command:
    userId: Snowflake
    name: str
    response: str
    guildId: Snowflake

    @staticmethod
    def parse_trigger(message: str) -> str:
        command_trigger = message[1:].split()[0]
        return command_trigger


class CommandManager:

    def __init__(self, bot: Bot, prisma: PrismaExt) -> None:
        self.client = bot
        self.prisma = prisma

    async def get_commands(self, guildId: Snowflake) -> List[Command]:
        command_objs: List[Command_MDL] = await self.prisma.where_many("command_mdl", 'guildId', int(guildId))
        commands = [await self.get_command(command_obj.name, command_obj.guildId) for command_obj in command_objs]
        return commands

    async def retrieve_response(self, command_name: str, guild_id: Snowflake) -> Union[str, None]:
        try:
            command_obj = await self.get_command(command_name, int(guild_id))
            return command_obj.response
        except IndexError as e:
            return

    async def commands_embed(self, guild_id: Snowflake):
        commands = await self.get_commands(int(guild_id))
        embed = Embed(title="Custom Commands", color=Color.blue())
        for command_obj in commands:
            embed.add_field(name=command_obj.name, value=command_obj.response)
        return embed

    async def create_command(self, command: Command) -> Command_MDL:
        name_mention = _RegexExp.ROLE_MENTION.match(command.name)
        response_mention = _RegexExp.ROLE_MENTION.match(command.response)
        if not name_mention and not response_mention:
            try:
                has_command = await self.prisma.where_unique("command_mdl", "name", "guildId",
                                                             command.name, command.guildId)
                raise UniqueException(f"Pre-existing command with name: {command.name}")
            except IndexError as e:
                command_obj = await self.prisma.command_mdl.create(
                    data={
                        'userId': int(command.userId),
                        'name': command.name,
                        'response': command.response,
                        'guildId': int(command.guildId)
                    }
                )
                return command_obj
        raise RoleMentionException(f"Mention of roles cannot be in name or response")

    async def remove_command(self, command: Command) -> Command_MDL:
        command_obj = await self.prisma.command_mdl.delete_many(
            where={
                'name': command.name,
                'guildId': command.guildId
            }
        )
        return command_obj

    async def get_command(self, name: str, guildId: Snowflake) -> Command:
        data: Command_MDL = await self.prisma.where_unique("command_mdl", 'name', 'guildId', name, guildId)
        command = Command(data.userId, data.name, data.response, data.guildId)
        return command
