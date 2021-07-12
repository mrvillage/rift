from __future__ import annotations

import inspect
import re
import sys
from typing import Any, Dict, List, Optional, Tuple, Type

from discord.ext.commands import Flag, FlagConverter, MissingFlagArgument
from discord.ext.commands.flags import get_flags, validate_flag_name
from discord.utils import MISSING


class BaseFlagConverter(FlagConverter):
    pass


class BooleanFlagConverter(BaseFlagConverter):
    @classmethod
    def parse_flags(cls, argument: str) -> Dict[str, List[str]]:
        result: Dict[str, List[str]] = {}
        flags = cls.__commands_flags__
        aliases = cls.__commands_flag_aliases__
        last_position = 0
        last_flag: Optional[Flag] = None

        case_insensitive = cls.__commands_flag_case_insensitive__
        for match in cls.__commands_flag_regex__.finditer(argument):
            begin, end = match.span(0)
            key = match.group("flag")
            if case_insensitive:
                key = key.casefold()

            if key in aliases:
                key = aliases[key]

            flag = flags.get(key)
            if last_position and last_flag is not None:
                value = argument[last_position : begin - 1].lstrip()
                if not value:
                    value = True
                    # raise MissingFlagArgument(last_flag)

                try:
                    values = result[last_flag.name]
                except KeyError:
                    result[last_flag.name] = [value]
                else:
                    values.append(value)

            last_position = end
            last_flag = flag

        # Add the remaining string to the last available flag
        if last_position and last_flag is not None:
            value = argument[last_position:].strip()
            if not value:
                value = True
                # raise MissingFlagArgument(last_flag)

            try:
                values = result[last_flag.name]
            except KeyError:
                result[last_flag.name] = [value]
            else:
                values.append(value)

        # Verification of values will come at a later stage
        return result
