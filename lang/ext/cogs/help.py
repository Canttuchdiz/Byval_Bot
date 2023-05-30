from discord import Embed, Color
from discord.ext.commands import Cog, command, Bot, Context


class HelpCog(Cog):

    def __int__(self, bot: Bot) -> None:
        self.client = bot

    @command()
    async def help(self, ctx: Context) -> None:
        embed = Embed(
            title="Byval Help",
            description="<:botdev:1110739529696018602> *Byval bot is a multipurpose bot, "
                        "with a specialty of evaluating code.*\n\n"
                        "**To perform an ``!eval`` operation follow the example below:**\n"
                        "!eval \`\`\`(lang)\nprint('Hello World')\n\`\`\`\n\n"
                        "You can do ``/command`` to see the custom command options.\n"
                        "The prefix is ``?`` for custom commands!\n\n"
                        "**You can also create and delete automod rules via the group ``/rule``!**\n\n"
                        "[**Add Me To Your Server!**](https://discord.com/api/oauth2/authorize?client_id"
                        "=1105318211718754314&"
                        "permissions=277025778784&scope=bot%20applications.commands)",
            color=Color.blue()
        )
        embed.set_footer(text="Prefix: ! · Read the descriptions of the commands to learn more")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
