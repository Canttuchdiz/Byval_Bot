from discord import Embed, Color
from enum import Enum


class _Lang(Enum):
    python = "py"
    csharp = "cs"
    c = "c"
    js = "js"


class _Embeds:
    embms = "{0} Runtime"
    embnl = "Invalid Language: {0}"
    embs = {True: Embed(title="Execution Completed", color=Color.green()),
            False: Embed(title="Execution Error", color=Color.red()),
            str: Embed(title="Compilation Error", color=Color.red())}
