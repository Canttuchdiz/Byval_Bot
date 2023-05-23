from discord import Embed, Color
from discord.ext.commands import Cog, command, Bot, Context
from discord import HTTPException
from lang.ext.models.pyston_ext import Pyston, _Lang
from lang.ext.models.formatter import Formatter


class Langs(Cog):

    def __int__(self, bot: Bot) -> None:
        self.bot = bot

    @command(name="eval")
    async def evaluate(self, ctx: Context, *, lang: str) -> None:
        client = Pyston()
        output = await client.run(lang)
        try:
            embed: Embed = Formatter.out_format(output)
            await ctx.send(embed=embed)
        except HTTPException as e:
            await ctx.send("Process output surpasses embed character limit.")

    @command(name="langs")
    async def langs(self, ctx: Context) -> None:
        embed = Embed(title="Languages", description=f"*{len(_Lang)//10*10}+ langs supported!*", color=Color.yellow())
        aclangs = ', '.join([lang.name.capitalize() for lang in _Lang])
        embed.add_field(name="Active", value=aclangs)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Langs(bot))
