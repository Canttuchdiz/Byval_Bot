from discord import Embed
from pyston.models import Output
from lang.utils.constants import _Embeds
from typing import Union


class Formatter:

    @staticmethod
    def out_format(output: Union[str, Output]) -> Embed:
        if isinstance(output, Output):
            embed = _Embeds.embs[output.success].copy()
            # embed.description = f"{_Embeds.embms.format(str(output.langauge).capitalize())}\n**{str(output)}**"
            embed.add_field(name=f"{_Embeds.embms.format(str(output.langauge).capitalize())}", value=str(output))
            return embed
        embed: Embed = _Embeds.embs[type(output)]
        embed.description = _Embeds.embnl.format(output.capitalize())
        return embed
