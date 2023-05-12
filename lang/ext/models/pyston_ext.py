from typing import Union

from pyston import PystonClient, File
from lang.utils.regex import Patterns
from pyston.models import Output
from pyston.exceptions import ExecutionError
from lang.utils.constants import _Lang


class Pyston(PystonClient):

    @staticmethod
    def get_lang(lang_abbr: str) -> Union[str, _Lang]:
        try:
            lang = _Lang(lang_abbr)
            return lang
        except ValueError as e:
            return lang_abbr

    async def run(self, source: str) -> Union[str, Output]:
        results = Patterns.re_match(Patterns.EVAL_REGEX, source, [1, 2])
        lang = self.get_lang(results[0])
        if isinstance(lang, _Lang):
            output = await self.execute(lang.name, [File(results[1])])
            return output
        return lang
