from __future__ import annotations
import asyncio
import aiofiles
from discord.ext.commands import Cog
from pydantic import BaseModel
import json
import prisma
import traceback
from typing import Any, List
import enum


class PrismaExt(prisma.Prisma):

    async def where_unique(self, table: str, column: str, un_column: str, item: str, un_item: str) -> List[BaseModel]:

        table_obj = getattr(self, table)

        data = await table_obj.find_many(
            where={
                column: item,
                un_column: un_item
            }
        )

        return data[0]

    async def where_first(self, table: str, column: str, item: str) -> object:

        try:

            table_obj = getattr(self, table)

            data = await table_obj.find_first(

                where={
                    column: item
                },

            )

            return data

        except Exception as e:
            traceback.print_exc()

    async def swap(self, app_name: str, order1, order2, id1, id2):

        """
        Swaps id on question table
        """

        # reference_table = TableTypes.options[0]
        #
        # id = await self.where_first(reference_table, reference_table, app_name)

        await self.question.query_raw("UPDATE question SET id = ? where id = ?", (order2, id1))

        await self.question.query_raw("UPDATE question SET id = ? where id = ?", (order1, id2))

    async def relate(self, app_name: str, table1: str, table2: str, guildId: int):

        try:

            # id = await self.where_first(table1, table1, app_name)

            table_obj = getattr(self, table1)

            id = await table_obj.find_first(

                where={
                    table1: app_name,
                    "guildId": guildId
                },

            )

            result = await self.where_many(table2, 'applicationId', id.id)

            return result
        except Exception as e:
            traceback.print_exc()

    async def where_one(self, table: str, column: str, item: str) -> object:

        try:

            table_obj = getattr(self, table)

            data = await table_obj.find_unique(

                where={
                    column: item
                },

            )

            return data

        except Exception as e:
            traceback.print_exc()

    async def where_many(self, table: str, column: str, item: Any) -> List[object]:

        """
        You specify the column that you are looking for use of item name
        """

        try:

            table_obj = getattr(self, table)

            data = await table_obj.find_many(

                where={
                    column: item
                },

            )

            return data

        except Exception as e:
            traceback.print_exc()

    async def db_data(self, obj_name: str) -> list:

        """
        Returns all items in a table object
        """

        try:
            obj = getattr(self, obj_name)

            items = await obj.find_many()

            return items

        except Exception as e:
            traceback.print_exc()

    async def sql_executor(self, query: str) -> list:
        try:
            val = await self.query_raw(query)

            return val
        except Exception as e:
            traceback.print_exc()
