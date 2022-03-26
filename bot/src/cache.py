from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from . import db, enums, models

__all__ = ("cache",)

if TYPE_CHECKING:
    from typing import Any, Optional


class Cache:
    __slots__ = (
        "_accounts",
        "_alliances",
        "_alliance_auto_roles",
        "_alliance_settings",
        "_alliances_private",
        "_audit_checks",
        "_audit_configs",
        "_audit_log_configs",
        "_audit_logs",
        "_audit_runs",
        "_bankrecs",
        "_blitzes",
        "_blitz_targets",
        "_bounties",
        "_builds",
        "_cities",
        "_city_auto_roles",
        "_colors",
        "_conditional_auto_roles",
        "_conditions",
        "_embassy_configs",
        "_embassies",
        "_grants",
        "_guild_roles",
        "_guild_settings",
        "_inactive_alerts",
        "_interview_answers",
        "_interview_configs",
        "_interview_questions",
        "_interviews",
        "_mentions",
        "_menu_interfaces",
        "_menu_items",
        "_menus",
        "_nations",
        "_nations_private",
        "_reminders",
        "_roles",
        "_rosters",
        "_servers",
        "_server_submissions",
        "_subscriptions",
        "_tags",
        "_target_configs",
        "_target_raters",
        "_target_reminders",
        "_tax_brackets",
        "_ticket_configs",
        "_tickets",
        "_trades",
        "_transactions",
        "_treasures",
        "_treaties",
        "_users",
        "_war_attacks",
        "_war_room_configs",
        "_war_rooms",
        "_wars",
    )

    def __init__(self) -> None:
        self._accounts: dict[int, models.Account] = {}
        self._alliances: dict[int, models.Alliance] = {}
        self._alliance_auto_roles: dict[int, models.AllianceAutoRole] = {}
        self._alliance_settings: dict[int, models.AllianceSettings] = {}
        self._alliances_private: dict[int, models.AlliancePrivate] = {}
        self._audit_checks: dict[int, models.AuditCheck] = {}
        self._audit_configs: dict[int, models.AuditConfig] = {}
        self._audit_log_configs: dict[int, models.AuditLogConfig] = {}
        self._audit_logs: dict[int, models.AuditLog] = {}
        self._audit_runs: dict[int, models.AuditRun] = {}
        self._bankrecs: dict[int, models.Bankrec] = {}
        self._blitzes: dict[int, models.Blitz] = {}
        self._blitz_targets: dict[int, models.BlitzTarget] = {}
        self._bounties: dict[int, models.Bounty] = {}
        self._builds: dict[int, models.Build] = {}
        self._cities: dict[int, models.City] = {}
        self._city_auto_roles: dict[int, models.CityAutoRole] = {}
        self._colors: dict[enums.Color, models.Color] = {}
        self._conditional_auto_roles: dict[int, models.ConditionalAutoRole] = {}
        self._conditions: dict[int, models.Condition] = {}
        self._embassy_configs: dict[int, models.EmbassyConfig] = {}
        self._embassies: dict[int, models.Embassy] = {}
        self._grants: dict[int, models.Grant] = {}
        self._guild_roles: dict[int, models.GuildRole] = {}
        self._guild_settings: dict[int, models.GuildSettings] = {}
        self._inactive_alerts: dict[int, models.InactiveAlert] = {}
        self._interview_answers: dict[int, models.InterviewAnswer] = {}
        self._interview_configs: dict[int, models.InterviewConfig] = {}
        self._interview_questions: dict[int, models.InterviewQuestion] = {}
        self._interviews: dict[int, models.Interview] = {}
        self._mentions: dict[int, models.Mention] = {}
        self._menu_interfaces: dict[int, models.MenuInterface] = {}
        self._menu_items: dict[int, models.MenuItem] = {}
        self._menus: dict[int, models.Menu] = {}
        self._nations: dict[int, models.Nation] = {}
        self._nations_private: dict[int, models.NationPrivate] = {}
        # self._radiation: models.Radiation
        self._reminders: dict[int, models.Reminder] = {}
        self._roles: dict[int, models.Role] = {}
        self._rosters: dict[int, models.Roster] = {}
        self._servers: dict[int, models.Server] = {}
        self._server_submissions: dict[int, models.ServerSubmission] = {}
        self._subscriptions: dict[int, models.Subscription] = {}
        self._tags: dict[int, models.Tag] = {}
        self._target_configs: dict[int, models.TargetConfig] = {}
        self._target_raters: dict[int, models.TargetRater] = {}
        self._target_reminders: dict[int, models.TargetReminder] = {}
        self._tax_brackets: dict[int, models.TaxBracket] = {}
        self._ticket_configs: dict[int, models.TicketConfig] = {}
        self._tickets: dict[int, models.Ticket] = {}
        self._trades: dict[int, models.Trade] = {}
        self._transactions: dict[int, models.Transaction] = {}
        self._treasures: dict[str, models.Treasure] = {}
        self._treaties: dict[int, models.Treaty] = {}
        self._users: dict[int, models.User] = {}
        self._war_attacks: dict[int, models.WarAttack] = {}
        self._war_room_configs: dict[int, models.WarRoomConfig] = {}
        self._war_rooms: dict[int, models.WarRoom] = {}
        self._wars: dict[int, models.War] = {}

    async def initialize(self) -> None:
        models_ = [
            models.Account,
            models.Alliance,
            models.AllianceAutoRole,
            models.AllianceSettings,
            models.AlliancePrivate,
            models.AuditCheck,
            models.AuditConfig,
            models.AuditLogConfig,
            models.AuditLog,
            models.AuditRun,
            models.Bankrec,
            models.Blitz,
            models.BlitzTarget,
            models.Bounty,
            models.Build,
            models.City,
            models.CityAutoRole,
            models.Color,
            models.ConditionalAutoRole,
            models.Condition,
            models.EmbassyConfig,
            models.Embassy,
            models.Grant,
            models.GuildRole,
            models.GuildSettings,
            models.InactiveAlert,
            models.InterviewAnswer,
            models.InterviewConfig,
            models.InterviewQuestion,
            models.Interview,
            models.Mention,
            models.MenuInterface,
            models.MenuItem,
            models.Menu,
            models.Nation,
            models.NationPrivate,
            models.Reminder,
            models.Role,
            models.Roster,
            models.Server,
            models.ServerSubmission,
            models.Subscription,
            models.Tag,
            models.TargetConfig,
            models.TargetRater,
            models.TargetReminder,
            models.TaxBracket,
            models.TicketConfig,
            models.Ticket,
            models.Trade,
            models.Transaction,
            models.Treasure,
            models.Treaty,
            models.User,
            models.WarAttack,
            models.WarRoomConfig,
            models.WarRoom,
            models.War,
        ]
        data: list[Any] = []
        for i in range(0, len(models_), 10):
            data.extend(
                await asyncio.gather(
                    *(
                        db.query(f"SELECT * FROM {i.TABLE};")  # nosec
                        for i in models_[i : i + 10]
                    )
                )
            )
        for i, result in zip(models_, data):
            attr = getattr(self, f"_{i.TABLE}")
            for row in result:
                # too lazy to properly type this
                model = i.from_dict(row)
                attr[i.key if hasattr(i, "key") else model.id] = model  # type: ignore

    def clear(self) -> None:
        self._accounts.clear()
        self._alliances.clear()
        self._alliance_auto_roles.clear()
        self._alliance_settings.clear()
        self._alliances_private.clear()
        self._audit_checks.clear()
        self._audit_configs.clear()
        self._audit_log_configs.clear()
        self._audit_logs.clear()
        self._audit_runs.clear()
        self._bankrecs.clear()
        self._blitzes.clear()
        self._blitz_targets.clear()
        self._bounties.clear()
        self._builds.clear()
        self._cities.clear()
        self._city_auto_roles.clear()
        self._colors.clear()
        self._conditional_auto_roles.clear()
        self._conditions.clear()
        self._embassy_configs.clear()
        self._embassies.clear()
        self._grants.clear()
        self._guild_roles.clear()
        self._guild_settings.clear()
        self._inactive_alerts.clear()
        self._interview_answers.clear()
        self._interview_configs.clear()
        self._interview_questions.clear()
        self._interviews.clear()
        self._mentions.clear()
        self._menu_interfaces.clear()
        self._menu_items.clear()
        self._menus.clear()
        self._nations.clear()
        self._nations_private.clear()
        # self._radiation.clear()
        self._reminders.clear()
        self._roles.clear()
        self._rosters.clear()
        self._servers.clear()
        self._server_submissions.clear()
        self._subscriptions.clear()
        self._tags.clear()
        self._target_configs.clear()
        self._target_raters.clear()
        self._target_reminders.clear()
        self._tax_brackets.clear()
        self._ticket_configs.clear()
        self._tickets.clear()
        self._trades.clear()
        self._transactions.clear()
        self._treasures.clear()
        self._treaties.clear()
        self._users.clear()
        self._war_attacks.clear()
        self._war_room_configs.clear()
        self._war_rooms.clear()
        self._wars.clear()

    @property
    def accounts(self) -> set[models.Account]:
        return set(self._accounts.values())

    def add_account(self, account: models.Account, /) -> None:
        self._accounts[account.id] = account

    def get_account(self, id: int, /) -> Optional[models.Account]:
        return self._accounts.get(id)

    def remove_account(self, character: models.Account, /) -> None:
        del self._accounts[character.id]

    @property
    def alliances(self) -> set[models.Alliance]:
        return set(self._alliances.values())

    def add_alliance(self, alliance: models.Alliance, /) -> None:
        self._alliances[alliance.id] = alliance

    def get_alliance(self, id: int, /) -> Optional[models.Alliance]:
        return self._alliances.get(id)

    def remove_alliance(self, account: models.Alliance, /) -> None:
        del self._alliances[account.id]

    @property
    def alliance_auto_roles(self) -> set[models.AllianceAutoRole]:
        return set(self._alliance_auto_roles.values())

    def add_alliance_auto_role(
        self, alliance_auto_role: models.AllianceAutoRole, /
    ) -> None:
        self._alliance_auto_roles[alliance_auto_role.id] = alliance_auto_role

    def get_alliance_auto_role(self, id: int, /) -> Optional[models.AllianceAutoRole]:
        return self._alliance_auto_roles.get(id)

    def remove_alliance_auto_role(
        self, alliance_auto_role: models.AllianceAutoRole, /
    ) -> None:
        del self._alliance_auto_roles[alliance_auto_role.id]

    @property
    def alliance_settings(self) -> set[models.AllianceSettings]:
        return set(self._alliance_settings.values())

    def add_alliance_setting(
        self, alliance_setting: models.AllianceSettings, /
    ) -> None:
        self._alliance_settings[alliance_setting.alliance_id] = alliance_setting

    def get_alliance_setting(
        self, alliance_id: int, /
    ) -> Optional[models.AllianceSettings]:
        return self._alliance_settings.get(alliance_id)

    def remove_alliance_setting(
        self, alliance_setting: models.AllianceSettings, /
    ) -> None:
        del self._alliance_settings[alliance_setting.alliance_id]

    @property
    def alliances_private(self) -> set[models.AlliancePrivate]:
        return set(self._alliances_private.values())

    def add_alliance_private(self, alliance_private: models.AlliancePrivate, /) -> None:
        self._alliances_private[alliance_private.id] = alliance_private

    def get_alliance_private(self, id: int, /) -> Optional[models.AlliancePrivate]:
        return self._alliances_private.get(id)

    def remove_alliance_private(
        self, alliances_private: models.AlliancePrivate, /
    ) -> None:
        del self._alliances_private[alliances_private.id]

    @property
    def audit_checks(self) -> set[models.AuditCheck]:
        return set(self._audit_checks.values())

    def add_audit_check(self, audit_check: models.AuditCheck, /) -> None:
        self._audit_checks[audit_check.id] = audit_check

    def get_audit_check(self, id: int, /) -> Optional[models.AuditCheck]:
        return self._audit_checks.get(id)

    def remove_audit_check(self, audit_check: models.AuditCheck, /) -> None:
        del self._audit_checks[audit_check.id]

    @property
    def audit_configs(self) -> set[models.AuditConfig]:
        return set(self._audit_configs.values())

    def add_audit_config(self, audit_config: models.AuditConfig, /) -> None:
        self._audit_configs[audit_config.id] = audit_config

    def get_audit_config(self, id: int, /) -> Optional[models.AuditConfig]:
        return self._audit_configs.get(id)

    def remove_audit_config(self, audit_config: models.AuditConfig, /) -> None:
        del self._audit_configs[audit_config.id]

    @property
    def audit_log_configs(self) -> set[models.AuditLogConfig]:
        return set(self._audit_log_configs.values())

    def add_audit_log_config(self, audit_log_config: models.AuditLogConfig, /) -> None:
        self._audit_log_configs[audit_log_config.id] = audit_log_config

    def get_audit_log_config(self, id: int, /) -> Optional[models.AuditLogConfig]:
        return self._audit_log_configs.get(id)

    def remove_audit_log_config(
        self, audit_log_config: models.AuditLogConfig, /
    ) -> None:
        del self._audit_log_configs[audit_log_config.id]

    @property
    def audit_logs(self) -> set[models.AuditLog]:
        return set(self._audit_logs.values())

    def add_audit_log(self, audit_log: models.AuditLog, /) -> None:
        self._audit_logs[audit_log.id] = audit_log

    def get_audit_log(self, id: int, /) -> Optional[models.AuditLog]:
        return self._audit_logs.get(id)

    def remove_audit_log(self, audit_log: models.AuditLog, /) -> None:
        del self._audit_logs[audit_log.id]

    @property
    def audit_runs(self) -> set[models.AuditRun]:
        return set(self._audit_runs.values())

    def add_audit_run(self, audit_run: models.AuditRun, /) -> None:
        self._audit_runs[audit_run.id] = audit_run

    def get_audit_run(self, id: int, /) -> Optional[models.AuditRun]:
        return self._audit_runs.get(id)

    def remove_audit_run(self, audit_run: models.AuditRun, /) -> None:
        del self._audit_runs[audit_run.id]

    @property
    def bankrecs(self) -> set[models.Bankrec]:
        return set(self._bankrecs.values())

    def add_bankrec(self, bankrec: models.Bankrec, /) -> None:
        self._bankrecs[bankrec.id] = bankrec

    def get_bankrec(self, id: int, /) -> Optional[models.Bankrec]:
        return self._bankrecs.get(id)

    def remove_bankrec(self, bankrec: models.Bankrec, /) -> None:
        del self._bankrecs[bankrec.id]

    @property
    def blitzes(self) -> set[models.Blitz]:
        return set(self._blitzes.values())

    def add_blitz(self, blitz: models.Blitz, /) -> None:
        self._blitzes[blitz.id] = blitz

    def get_blitz(self, id: int, /) -> Optional[models.Blitz]:
        return self._blitzes.get(id)

    def remove_blitz(self, blitz: models.Blitz, /) -> None:
        del self._blitzes[blitz.id]

    @property
    def blitz_targets(self) -> set[models.BlitzTarget]:
        return set(self._blitz_targets.values())

    def add_blitz_target(self, blitz_target: models.BlitzTarget, /) -> None:
        self._blitz_targets[blitz_target.id] = blitz_target

    def get_blitz_target(self, id: int, /) -> Optional[models.BlitzTarget]:
        return self._blitz_targets.get(id)

    def remove_blitz_target(self, blitz_target: models.BlitzTarget, /) -> None:
        del self._blitz_targets[blitz_target.id]

    @property
    def bounties(self) -> set[models.Bounty]:
        return set(self._bounties.values())

    def add_bounty(self, bounty: models.Bounty, /) -> None:
        self._bounties[bounty.id] = bounty

    def get_bounty(self, id: int, /) -> Optional[models.Bounty]:
        return self._bounties.get(id)

    def remove_bounty(self, bounty: models.Bounty, /) -> None:
        del self._bounties[bounty.id]

    @property
    def builds(self) -> set[models.Build]:
        return set(self._builds.values())

    def add_build(self, build: models.Build, /) -> None:
        self._builds[build.id] = build

    def get_build(self, id: int, /) -> Optional[models.Build]:
        return self._builds.get(id)

    def remove_build(self, build: models.Build, /) -> None:
        del self._builds[build.id]

    @property
    def cities(self) -> set[models.City]:
        return set(self._cities.values())

    def add_city(self, city: models.City, /) -> None:
        self._cities[city.id] = city

    def get_city(self, id: int, /) -> Optional[models.City]:
        return self._cities.get(id)

    def remove_city(self, city: models.City, /) -> None:
        del self._cities[city.id]

    @property
    def city_auto_roles(self) -> set[models.CityAutoRole]:
        return set(self._city_auto_roles.values())

    def add_city_auto_role(self, city_auto_role: models.CityAutoRole, /) -> None:
        self._city_auto_roles[city_auto_role.id] = city_auto_role

    def get_city_auto_role(self, id: int, /) -> Optional[models.CityAutoRole]:
        return self._city_auto_roles.get(id)

    def remove_city_auto_role(self, city_auto_role: models.CityAutoRole, /) -> None:
        del self._city_auto_roles[city_auto_role.id]

    @property
    def colors(self) -> set[models.Color]:
        return set(self._colors.values())

    def add_color(self, color: models.Color, /) -> None:
        self._colors[color.color] = color

    def get_color(self, color: enums.Color, /) -> Optional[models.Color]:
        return self._colors.get(color)

    def remove_color(self, color: models.Color, /) -> None:
        del self._colors[color.color]

    @property
    def conditional_auto_roles(self) -> set[models.ConditionalAutoRole]:
        return set(self._conditional_auto_roles.values())

    def add_conditional_auto_role(
        self, conditional_auto_role: models.ConditionalAutoRole, /
    ) -> None:
        self._conditional_auto_roles[conditional_auto_role.id] = conditional_auto_role

    def get_conditional_auto_role(
        self, id: int, /
    ) -> Optional[models.ConditionalAutoRole]:
        return self._conditional_auto_roles.get(id)

    def remove_conditional_auto_role(
        self, conditional_auto_role: models.ConditionalAutoRole, /
    ) -> None:
        del self._conditional_auto_roles[conditional_auto_role.id]

    @property
    def conditions(self) -> set[models.Condition]:
        return set(self._conditions.values())

    def add_condition(self, condition: models.Condition, /) -> None:
        self._conditions[condition.id] = condition

    def get_condition(self, id: int, /) -> Optional[models.Condition]:
        return self._conditions.get(id)

    def remove_condition(self, condition: models.Condition, /) -> None:
        del self._conditions[condition.id]

    @property
    def embassy_configs(self) -> set[models.EmbassyConfig]:
        return set(self._embassy_configs.values())

    def add_embassy_config(self, embassy_config: models.EmbassyConfig, /) -> None:
        self._embassy_configs[embassy_config.id] = embassy_config

    def get_embassy_config(self, id: int, /) -> Optional[models.EmbassyConfig]:
        return self._embassy_configs.get(id)

    def remove_embassy_config(self, embassy_config: models.EmbassyConfig, /) -> None:
        del self._embassy_configs[embassy_config.id]

    @property
    def embassies(self) -> set[models.Embassy]:
        return set(self._embassies.values())

    def add_embassy(self, embassy: models.Embassy, /) -> None:
        self._embassies[embassy.id] = embassy

    def get_embassy(self, id: int, /) -> Optional[models.Embassy]:
        return self._embassies.get(id)

    def remove_embassy(self, embassy: models.Embassy, /) -> None:
        del self._embassies[embassy.id]

    @property
    def grants(self) -> set[models.Grant]:
        return set(self._grants.values())

    def add_grant(self, grant: models.Grant, /) -> None:
        self._grants[grant.id] = grant

    def get_grant(self, id: int, /) -> Optional[models.Grant]:
        return self._grants.get(id)

    def remove_grant(self, grant: models.Grant, /) -> None:
        del self._grants[grant.id]

    @property
    def guild_roles(self) -> set[models.GuildRole]:
        return set(self._guild_roles.values())

    def add_guild_role(self, guild_role: models.GuildRole, /) -> None:
        self._guild_roles[guild_role.id] = guild_role

    def get_guild_role(self, id: int, /) -> Optional[models.GuildRole]:
        return self._guild_roles.get(id)

    def remove_guild_role(self, guild_role: models.GuildRole, /) -> None:
        del self._guild_roles[guild_role.id]

    @property
    def guild_settings(self) -> set[models.GuildSettings]:
        return set(self._guild_settings.values())

    def add_guild_settings(self, guild_settings: models.GuildSettings, /) -> None:
        self._guild_settings[guild_settings.guild_id] = guild_settings

    def get_guild_settings(self, guild_id: int, /) -> Optional[models.GuildSettings]:
        return self._guild_settings.get(guild_id)

    def remove_guild_settings(self, guild_settings: models.GuildSettings, /) -> None:
        del self._guild_settings[guild_settings.guild_id]

    @property
    def inactive_alerts(self) -> set[models.InactiveAlert]:
        return set(self._inactive_alerts.values())

    def add_inactive_alert(self, inactive_alert: models.InactiveAlert, /) -> None:
        self._inactive_alerts[inactive_alert.nation_id] = inactive_alert

    def get_inactive_alert(self, id: int, /) -> Optional[models.InactiveAlert]:
        return self._inactive_alerts.get(id)

    def remove_inactive_alert(self, inactive_alert: models.InactiveAlert, /) -> None:
        del self._inactive_alerts[inactive_alert.nation_id]

    @property
    def interview_answers(self) -> set[models.InterviewAnswer]:
        return set(self._interview_answers.values())

    def add_interview_answer(self, interview_answer: models.InterviewAnswer, /) -> None:
        self._interview_answers[interview_answer.id] = interview_answer

    def get_interview_answer(self, id: int, /) -> Optional[models.InterviewAnswer]:
        return self._interview_answers.get(id)

    def remove_interview_answer(
        self, interview_answer: models.InterviewAnswer, /
    ) -> None:
        del self._interview_answers[interview_answer.id]

    @property
    def interview_configs(self) -> set[models.InterviewConfig]:
        return set(self._interview_configs.values())

    def add_interview_config(self, interview_config: models.InterviewConfig, /) -> None:
        self._interview_configs[interview_config.id] = interview_config

    def get_interview_config(self, id: int, /) -> Optional[models.InterviewConfig]:
        return self._interview_configs.get(id)

    def remove_interview_config(
        self, interview_config: models.InterviewConfig, /
    ) -> None:
        del self._interview_configs[interview_config.id]

    @property
    def interview_questions(self) -> set[models.InterviewQuestion]:
        return set(self._interview_questions.values())

    def add_interview_question(
        self, interview_question: models.InterviewQuestion, /
    ) -> None:
        self._interview_questions[interview_question.id] = interview_question

    def get_interview_question(self, id: int, /) -> Optional[models.InterviewQuestion]:
        return self._interview_questions.get(id)

    def remove_interview_question(
        self, interview_question: models.InterviewQuestion, /
    ) -> None:
        del self._interview_questions[interview_question.id]

    @property
    def interviews(self) -> set[models.Interview]:
        return set(self._interviews.values())

    def add_interview(self, interview: models.Interview, /) -> None:
        self._interviews[interview.id] = interview

    def get_interview(self, id: int, /) -> Optional[models.Interview]:
        return self._interviews.get(id)

    def remove_interview(self, interview: models.Interview, /) -> None:
        del self._interviews[interview.id]

    @property
    def mentions(self) -> set[models.Mention]:
        return set(self._mentions.values())

    def add_mention(self, mention: models.Mention, /) -> None:
        self._mentions[mention.id] = mention

    def get_mention(self, id: int, /) -> Optional[models.Mention]:
        return self._mentions.get(id)

    def remove_mention(self, mention: models.Mention, /) -> None:
        del self._mentions[mention.id]

    @property
    def menu_interfaces(self) -> set[models.MenuInterface]:
        return set(self._menu_interfaces.values())

    def add_menu_interface(self, menu_interface: models.MenuInterface, /) -> None:
        self._menu_interfaces[menu_interface.id] = menu_interface

    def get_menu_interface(self, id: int, /) -> Optional[models.MenuInterface]:
        return self._menu_interfaces.get(id)

    def remove_menu_interface(self, menu_interface: models.MenuInterface, /) -> None:
        del self._menu_interfaces[menu_interface.id]

    @property
    def menu_items(self) -> set[models.MenuItem]:
        return set(self._menu_items.values())

    def add_menu_item(self, menu_item: models.MenuItem, /) -> None:
        self._menu_items[menu_item.id] = menu_item

    def get_menu_item(self, id: int, /) -> Optional[models.MenuItem]:
        return self._menu_items.get(id)

    def remove_menu_item(self, menu_item: models.MenuItem, /) -> None:
        del self._menu_items[menu_item.id]

    @property
    def menus(self) -> set[models.Menu]:
        return set(self._menus.values())

    def add_menu(self, menu: models.Menu, /) -> None:
        self._menus[menu.id] = menu

    def get_menu(self, id: int, /) -> Optional[models.Menu]:
        return self._menus.get(id)

    def remove_menu(self, menu: models.Menu, /) -> None:
        del self._menus[menu.id]

    @property
    def nations(self) -> set[models.Nation]:
        return set(self._nations.values())

    def add_nation(self, nation: models.Nation, /) -> None:
        self._nations[nation.id] = nation

    def get_nation(self, id: int, /) -> Optional[models.Nation]:
        return self._nations.get(id)

    def remove_nation(self, nation: models.Nation, /) -> None:
        del self._nations[nation.id]

    @property
    def nations_private(self) -> set[models.NationPrivate]:
        return set(self._nations_private.values())

    def add_nation_private(self, nation_private: models.NationPrivate, /) -> None:
        self._nations_private[nation_private.id] = nation_private

    def get_nation_private(self, id: int, /) -> Optional[models.NationPrivate]:
        return self._nations_private.get(id)

    def remove_nation_private(self, nations_private: models.NationPrivate, /) -> None:
        del self._nations_private[nations_private.id]

    @property
    def reminders(self) -> set[models.Reminder]:
        return set(self._reminders.values())

    def add_reminder(self, reminder: models.Reminder, /) -> None:
        self._reminders[reminder.id] = reminder

    def get_reminder(self, id: int, /) -> Optional[models.Reminder]:
        return self._reminders.get(id)

    def remove_reminder(self, reminder: models.Reminder, /) -> None:
        del self._reminders[reminder.id]

    @property
    def roles(self) -> set[models.Role]:
        return set(self._roles.values())

    def add_role(self, role: models.Role, /) -> None:
        self._roles[role.id] = role

    def get_role(self, id: int, /) -> Optional[models.Role]:
        return self._roles.get(id)

    def remove_role(self, role: models.Role, /) -> None:
        del self._roles[role.id]

    @property
    def rosters(self) -> set[models.Roster]:
        return set(self._rosters.values())

    def add_roster(self, roster: models.Roster, /) -> None:
        self._rosters[roster.id] = roster

    def get_roster(self, id: int, /) -> Optional[models.Roster]:
        return self._rosters.get(id)

    def remove_roster(self, roster: models.Roster, /) -> None:
        del self._rosters[roster.id]

    @property
    def servers(self) -> set[models.Server]:
        return set(self._servers.values())

    def add_server(self, server: models.Server, /) -> None:
        self._servers[server.id] = server

    def get_server(self, id: int, /) -> Optional[models.Server]:
        return self._servers.get(id)

    def remove_server(self, server: models.Server, /) -> None:
        del self._servers[server.id]

    @property
    def server_submissions(self) -> set[models.ServerSubmission]:
        return set(self._server_submissions.values())

    def add_server_submission(
        self, server_submission: models.ServerSubmission, /
    ) -> None:
        self._server_submissions[server_submission.id] = server_submission

    def get_server_submission(self, id: int, /) -> Optional[models.ServerSubmission]:
        return self._server_submissions.get(id)

    def remove_server_submission(
        self, server_submission: models.ServerSubmission, /
    ) -> None:
        del self._server_submissions[server_submission.id]

    @property
    def subscriptions(self) -> set[models.Subscription]:
        return set(self._subscriptions.values())

    def add_subscription(self, subscription: models.Subscription, /) -> None:
        self._subscriptions[subscription.id] = subscription

    def get_subscription(self, id: int, /) -> Optional[models.Subscription]:
        return self._subscriptions.get(id)

    def remove_subscription(self, subscription: models.Subscription, /) -> None:
        del self._subscriptions[subscription.id]

    @property
    def tags(self) -> set[models.Tag]:
        return set(self._tags.values())

    def add_tag(self, tag: models.Tag, /) -> None:
        self._tags[tag.id] = tag

    def get_tag(self, id: int, /) -> Optional[models.Tag]:
        return self._tags.get(id)

    def remove_tag(self, tag: models.Tag, /) -> None:
        del self._tags[tag.id]

    @property
    def target_configs(self) -> set[models.TargetConfig]:
        return set(self._target_configs.values())

    def add_target_config(self, target_config: models.TargetConfig, /) -> None:
        self._target_configs[target_config.id] = target_config

    def get_target_config(self, id: int, /) -> Optional[models.TargetConfig]:
        return self._target_configs.get(id)

    def remove_target_config(self, target_config: models.TargetConfig, /) -> None:
        del self._target_configs[target_config.id]

    @property
    def target_raters(self) -> set[models.TargetRater]:
        return set(self._target_raters.values())

    def add_target_rater(self, target_rater: models.TargetRater, /) -> None:
        self._target_raters[target_rater.id] = target_rater

    def get_target_rater(self, id: int, /) -> Optional[models.TargetRater]:
        return self._target_raters.get(id)

    def remove_target_rater(self, target_rater: models.TargetRater, /) -> None:
        del self._target_raters[target_rater.id]

    @property
    def target_reminders(self) -> set[models.TargetReminder]:
        return set(self._target_reminders.values())

    def add_target_reminder(self, target_reminder: models.TargetReminder, /) -> None:
        self._target_reminders[target_reminder.id] = target_reminder

    def get_target_reminder(self, id: int, /) -> Optional[models.TargetReminder]:
        return self._target_reminders.get(id)

    def remove_target_reminder(self, target_reminder: models.TargetReminder, /) -> None:
        del self._target_reminders[target_reminder.id]

    @property
    def tax_brackets(self) -> set[models.TaxBracket]:
        return set(self._tax_brackets.values())

    def add_tax_bracket(self, tax_bracket: models.TaxBracket, /) -> None:
        self._tax_brackets[tax_bracket.id] = tax_bracket

    def get_tax_bracket(self, id: int, /) -> Optional[models.TaxBracket]:
        return self._tax_brackets.get(id)

    def remove_tax_bracket(self, tax_bracket: models.TaxBracket, /) -> None:
        del self._tax_brackets[tax_bracket.id]

    @property
    def ticket_configs(self) -> set[models.TicketConfig]:
        return set(self._ticket_configs.values())

    def add_ticket_config(self, ticket_config: models.TicketConfig, /) -> None:
        self._ticket_configs[ticket_config.id] = ticket_config

    def get_ticket_config(self, id: int, /) -> Optional[models.TicketConfig]:
        return self._ticket_configs.get(id)

    def remove_ticket_config(self, ticket_config: models.TicketConfig, /) -> None:
        del self._ticket_configs[ticket_config.id]

    @property
    def tickets(self) -> set[models.Ticket]:
        return set(self._tickets.values())

    def add_ticket(self, ticket: models.Ticket, /) -> None:
        self._tickets[ticket.id] = ticket

    def get_ticket(self, id: int, /) -> Optional[models.Ticket]:
        return self._tickets.get(id)

    def remove_ticket(self, ticket: models.Ticket, /) -> None:
        del self._tickets[ticket.id]

    @property
    def trades(self) -> set[models.Trade]:
        return set(self._trades.values())

    def add_trade(self, trade: models.Trade, /) -> None:
        self._trades[trade.id] = trade

    def get_trade(self, id: int, /) -> Optional[models.Trade]:
        return self._trades.get(id)

    def remove_trade(self, trade: models.Trade, /) -> None:
        del self._trades[trade.id]

    @property
    def transactions(self) -> set[models.Transaction]:
        return set(self._transactions.values())

    def add_transaction(self, transaction: models.Transaction, /) -> None:
        self._transactions[transaction.id] = transaction

    def get_transaction(self, id: int, /) -> Optional[models.Transaction]:
        return self._transactions.get(id)

    def remove_transaction(self, transaction: models.Transaction, /) -> None:
        del self._transactions[transaction.id]

    @property
    def treasures(self) -> set[models.Treasure]:
        return set(self._treasures.values())

    def add_treasure(self, treasure: models.Treasure, /) -> None:
        self._treasures[treasure.name] = treasure

    def get_treasure(self, name: str, /) -> Optional[models.Treasure]:
        return self._treasures.get(name)

    def remove_treasure(self, treasure: models.Treasure, /) -> None:
        del self._treasures[treasure.name]

    @property
    def treaties(self) -> set[models.Treaty]:
        return set(self._treaties.values())

    def add_treaty(self, treaty: models.Treaty, /) -> None:
        self._treaties[treaty.id] = treaty

    def get_treaty(self, id: int, /) -> Optional[models.Treaty]:
        return self._treaties.get(id)

    def remove_treaty(self, treaty: models.Treaty, /) -> None:
        del self._treaties[treaty.id]

    @property
    def users(self) -> set[models.User]:
        return set(self._users.values())

    def add_user(self, user: models.User, /) -> None:
        self._users[user.user_id] = user

    def get_user(self, id: int, /) -> Optional[models.User]:
        return self._users.get(id)

    def remove_user(self, user: models.User, /) -> None:
        del self._users[user.user_id]

    @property
    def war_attacks(self) -> set[models.WarAttack]:
        return set(self._war_attacks.values())

    def add_war_attack(self, war_attack: models.WarAttack, /) -> None:
        self._war_attacks[war_attack.id] = war_attack

    def get_war_attack(self, id: int, /) -> Optional[models.WarAttack]:
        return self._war_attacks.get(id)

    def remove_war_attack(self, war_attack: models.WarAttack, /) -> None:
        del self._war_attacks[war_attack.id]

    @property
    def war_room_configs(self) -> set[models.WarRoomConfig]:
        return set(self._war_room_configs.values())

    def add_war_room_config(self, war_room_config: models.WarRoomConfig, /) -> None:
        self._war_room_configs[war_room_config.id] = war_room_config

    def get_war_room_config(self, id: int, /) -> Optional[models.WarRoomConfig]:
        return self._war_room_configs.get(id)

    def remove_war_room_config(self, war_room_config: models.WarRoomConfig, /) -> None:
        del self._war_room_configs[war_room_config.id]

    @property
    def war_rooms(self) -> set[models.WarRoom]:
        return set(self._war_rooms.values())

    def add_war_room(self, war_room: models.WarRoom, /) -> None:
        self._war_rooms[war_room.id] = war_room

    def get_war_room(self, id: int, /) -> Optional[models.WarRoom]:
        return self._war_rooms.get(id)

    def remove_war_room(self, war_room: models.WarRoom, /) -> None:
        del self._war_rooms[war_room.id]

    @property
    def wars(self) -> set[models.War]:
        return set(self._wars.values())

    def add_war(self, war: models.War, /) -> None:
        self._wars[war.id] = war

    def get_war(self, id: int, /) -> Optional[models.War]:
        return self._wars.get(id)

    def remove_war(self, war: models.War, /) -> None:
        del self._wars[war.id]


cache = Cache()


def __getattr__(name: str) -> Any:
    return getattr(cache, name)
