from __future__ import annotations

from typing import TYPE_CHECKING

from .. import utils

__all__ = (
    "COMMAND_IS_GUILD_ONLY",
    "CREATED",
    "model_created_at",
    "not_found",
    "enum_name",
    "SUPPORT_SERVER",
    "FATAL_ERROR",
    "NONE",
    "click_here_link_or_none",
    "missing_discord_permissions",
    "model_created_id",
    "model_deleted_id",
    "model_edited_id",
    "model_created",
    "model_deleted",
    "model_edited",
    "model_list",
)

if TYPE_CHECKING:
    import enum
    from typing import Any, Final, Optional

COMMAND_IS_GUILD_ONLY: Final[str] = "Sorry, this command can only be used in a server!"
CREATED: Final[str] = "Created"


def model_created_at(model: str) -> str:
    return f"{model} created!"


def not_found(name: str, value: Optional[str], infer: bool = False) -> str:
    if value is None and infer:
        return f"Your Discord account is not linked to a nation so I couldn't infer your {name}!"
    return f"No {name} found with argument `{value}`."


def enum_name(value: enum.Enum) -> str:
    return utils.snake_case_to_capitals(value.name)


SUPPORT_SERVER = "https://rift.mrvillage.dev/discord"
FATAL_ERROR: Final[
    str
] = f"Uh oh! Something went wrong! Please try again later. If you need further assistance or the problem persists please join the support server [here]({SUPPORT_SERVER}) or context <@258298021266063360>."
NONE: Final[str] = "None"


def click_here_link_or_none(link: Optional[str]) -> str:
    return f"[Click here]({link})" if link else "None"


def missing_discord_permissions(permissions: dict[str, bool]) -> str:
    return f"You need the following permissions to do that!\n{', '.join(f'`{utils.snake_case_to_capitals(permission)}`' for permission, has_permission in permissions.items() if not has_permission)}"


def model_created_id(model: str, id: int) -> str:
    return f"{model} successfully created with ID {id}!"


def model_deleted_id(model: str, id: int) -> str:
    return f"{model} with ID {id} successfully deleted!"


def model_edited_id(model: str, id: int) -> str:
    return f"{model} with ID {id} successfully edited!"


def model_created(model: str, value: Any) -> str:
    return f"{model} {value} successfully created!"


def model_deleted(model: str, value: Any) -> str:
    return f"{model} {value} successfully deleted!"


def model_edited(model: str, value: Any) -> str:
    return f"{model} {value} successfully edited!"


def model_list(
    singular: str, values: list[Any], *, plural: Optional[str] = None
) -> str:
    plural = plural or f"{singular}s"
    length = len(values)
    if length == 0:
        return f"No {plural} found!"
    joined = "\n".join(f"{index + 1}. {value}" for index, value in enumerate(values))
    if length == 1:
        return f"{length:,} {singular} found!\n\n{joined}"
    return f"{length:,} {plural} found!\n\n{joined}"
