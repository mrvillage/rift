from __future__ import annotations

from typing import TYPE_CHECKING

__all__ = (
    "COMMAND_IS_GUILD_ONLY",
    "CREATED",
    "model_created",
    "not_found",
    "enum_name",
    "SUPPORT_SERVER",
    "FATAL_ERROR",
)

if TYPE_CHECKING:
    import enum
    from typing import Final, Optional

COMMAND_IS_GUILD_ONLY: Final[str] = "Sorry, this command can only be used in a server!"
CREATED: Final[str] = "Created"


def model_created(model: str) -> str:
    return f"{model} created!"


def not_found(name: str, value: Optional[str], infer: bool = False) -> str:
    if value is None and infer:
        return f"Your Discord account is not linked to a nation so I couldn't infer your {name}!"
    return f"No {name} found with argument `{value}`."


def enum_name(value: enum.Enum) -> str:
    return " ".join(i.capitalize() for i in value.name.split("_"))


SUPPORT_SERVER = "https://rift.mrvillage.dev/discord"
FATAL_ERROR: Final[
    str
] = f"Uh oh! Something went wrong! Please try again later. If you need further assistance or the problem persists please join the support server [here]({SUPPORT_SERVER}) or context <@258298021266063360>."
