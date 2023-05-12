from re import Pattern, compile, DOTALL, IGNORECASE
from lang.utils.errors import InvalidGroup
from typing import List


class Patterns:

    @staticmethod
    def re_match(pattern: Pattern, src: str, groups: List[int]) -> List[str]:
        result = pattern.match(src)
        results = []
        try:
            for group in groups:
                results.append(result.group(group))
        except IndexError as e:
            raise InvalidGroup(f"Invalid group number")
        return results

    EVAL_REGEX = compile(
        r'```(?:(?P<language>\w*)\n)?\s*(?P<code>.*?)\s*```',
        IGNORECASE | DOTALL
    )
