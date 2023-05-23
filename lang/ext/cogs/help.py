from discord import Embed, Color
from discord.ext.commands import Cog, command, Bot, Context


class HelpCog(Cog):

    def __int__(self, bot: Bot) -> None:
        self.client = bot

    @command()
    async def help(self, ctx: Context) -> None:
        embed = Embed(
            title="Byval Help",
            description="*Byval bot is a multipurpose bot, with a specialty of evaluating code.*\n\n"
                        "**To perform an ``!eval`` operation follow the example below:**\n"
                        "!eval \`\`\`(lang)\nprint('Hello World')\n\`\`\`\n\n"
                        "**You can also create automod rules via ``/rule create``!**\n"
                        "Read the descriptions of the command to learn more.",
            color=Color.blue()
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
