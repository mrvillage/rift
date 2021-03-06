# flake8: noqa
# pycodestyle: noqa

from __future__ import annotations

from typing import TYPE_CHECKING

from . import enums, models

if TYPE_CHECKING:
    from typing import Optional

async def initialize() -> None: ...
def clear() -> None: ...

accounts: set[models.Account]

def add_account(account: models.Account, /) -> None: ...
def get_account(id: int, /) -> Optional[models.Account]: ...
def remove_account(character: models.Account, /) -> None: ...

alliances: set[models.Alliance]

def add_alliance(alliance: models.Alliance, /) -> None: ...
def get_alliance(id: int, /) -> Optional[models.Alliance]: ...
def remove_alliance(account: models.Alliance, /) -> None: ...

alliance_auto_roles: set[models.AllianceAutoRole]

def add_alliance_auto_role(alliance_auto_role: models.AllianceAutoRole, /) -> None: ...
def get_alliance_auto_role(id: int, /) -> Optional[models.AllianceAutoRole]: ...
def remove_alliance_auto_role(
    alliance_auto_role: models.AllianceAutoRole, /
) -> None: ...

alliance_settings: set[models.AllianceSettings]

def add_alliance_setting(alliance_setting: models.AllianceSettings, /) -> None: ...
def get_alliance_setting(alliance_id: int, /) -> Optional[models.AllianceSettings]: ...
def remove_alliance_setting(alliance_setting: models.AllianceSettings, /) -> None: ...

alliances_private: set[models.AlliancePrivate]

def add_alliance_private(alliance_private: models.AlliancePrivate, /) -> None: ...
def get_alliance_private(id: int, /) -> Optional[models.AlliancePrivate]: ...
def remove_alliance_private(alliances_private: models.AlliancePrivate, /) -> None: ...

audit_checks: set[models.AuditCheck]

def add_audit_check(audit_check: models.AuditCheck, /) -> None: ...
def get_audit_check(id: int, /) -> Optional[models.AuditCheck]: ...
def remove_audit_check(audit_check: models.AuditCheck, /) -> None: ...

audit_configs: set[models.AuditConfig]

def add_audit_config(audit_config: models.AuditConfig, /) -> None: ...
def get_audit_config(id: int, /) -> Optional[models.AuditConfig]: ...
def remove_audit_config(audit_config: models.AuditConfig, /) -> None: ...

audit_log_configs: set[models.AuditLogConfig]

def add_audit_log_config(audit_log_config: models.AuditLogConfig, /) -> None: ...
def get_audit_log_config(id: int, /) -> Optional[models.AuditLogConfig]: ...
def remove_audit_log_config(audit_log_config: models.AuditLogConfig, /) -> None: ...

audit_logs: set[models.AuditLog]

def add_audit_log(audit_log: models.AuditLog, /) -> None: ...
def get_audit_log(id: int, /) -> Optional[models.AuditLog]: ...
def remove_audit_log(audit_log: models.AuditLog, /) -> None: ...

audit_runs: set[models.AuditRun]

def add_audit_run(audit_run: models.AuditRun, /) -> None: ...
def get_audit_run(id: int, /) -> Optional[models.AuditRun]: ...
def remove_audit_run(audit_run: models.AuditRun, /) -> None: ...

bankrecs: set[models.Bankrec]

def add_bankrec(bankrec: models.Bankrec, /) -> None: ...
def get_bankrec(id: int, /) -> Optional[models.Bankrec]: ...
def remove_bankrec(bankrec: models.Bankrec, /) -> None: ...

blitzes: set[models.Blitz]

def add_blitz(blitz: models.Blitz, /) -> None: ...
def get_blitz(id: int, /) -> Optional[models.Blitz]: ...
def remove_blitz(blitz: models.Blitz, /) -> None: ...

blitz_targets: set[models.BlitzTarget]

def add_blitz_target(blitz_target: models.BlitzTarget, /) -> None: ...
def get_blitz_target(id: int, /) -> Optional[models.BlitzTarget]: ...
def remove_blitz_target(blitz_target: models.BlitzTarget, /) -> None: ...

bounties: set[models.Bounty]

def add_bounty(bounty: models.Bounty, /) -> None: ...
def get_bounty(id: int, /) -> Optional[models.Bounty]: ...
def remove_bounty(bounty: models.Bounty, /) -> None: ...

builds: set[models.Build]

def add_build(build: models.Build, /) -> None: ...
def get_build(id: int, /) -> Optional[models.Build]: ...
def remove_build(build: models.Build, /) -> None: ...

cities: set[models.City]

def add_city(city: models.City, /) -> None: ...
def get_city(id: int, /) -> Optional[models.City]: ...
def remove_city(city: models.City, /) -> None: ...

city_auto_roles: set[models.CityAutoRole]

def add_city_auto_role(city_auto_role: models.CityAutoRole, /) -> None: ...
def get_city_auto_role(id: int, /) -> Optional[models.CityAutoRole]: ...
def remove_city_auto_role(city_auto_role: models.CityAutoRole, /) -> None: ...

colors: set[models.Color]

def add_color(color: models.Color, /) -> None: ...
def get_color(color: enums.Color, /) -> Optional[models.Color]: ...
def remove_color(color: models.Color, /) -> None: ...

conditional_auto_roles: set[models.ConditionalAutoRole]

def add_conditional_auto_role(
    conditional_auto_role: models.ConditionalAutoRole, /
) -> None: ...
def get_conditional_auto_role(id: int, /) -> Optional[models.ConditionalAutoRole]: ...
def remove_conditional_auto_role(
    conditional_auto_role: models.ConditionalAutoRole, /
) -> None: ...

conditions: set[models.Condition]

def add_condition(condition: models.Condition, /) -> None: ...
def get_condition(id: int, /) -> Optional[models.Condition]: ...
def remove_condition(condition: models.Condition, /) -> None: ...

embassy_configs: set[models.EmbassyConfig]

def add_embassy_config(embassy_config: models.EmbassyConfig, /) -> None: ...
def get_embassy_config(id: int, /) -> Optional[models.EmbassyConfig]: ...
def remove_embassy_config(embassy_config: models.EmbassyConfig, /) -> None: ...

embassies: set[models.Embassy]

def add_embassy(embassy: models.Embassy, /) -> None: ...
def get_embassy(id: int, /) -> Optional[models.Embassy]: ...
def remove_embassy(embassy: models.Embassy, /) -> None: ...

grants: set[models.Grant]

def add_grant(grant: models.Grant, /) -> None: ...
def get_grant(id: int, /) -> Optional[models.Grant]: ...
def remove_grant(grant: models.Grant, /) -> None: ...

guild_roles: set[models.GuildRole]

def add_guild_role(guild_role: models.GuildRole, /) -> None: ...
def get_guild_role(id: int, /) -> Optional[models.GuildRole]: ...
def remove_guild_role(guild_role: models.GuildRole, /) -> None: ...

guild_settings: set[models.GuildSettings]

def add_guild_settings(guild_settings: models.GuildSettings, /) -> None: ...
def get_guild_settings(guild_id: int, /) -> Optional[models.GuildSettings]: ...
def remove_guild_settings(guild_settings: models.GuildSettings, /) -> None: ...

inactive_alerts: set[models.InactiveAlert]

def add_inactive_alert(inactive_alert: models.InactiveAlert, /) -> None: ...
def get_inactive_alert(id: int, /) -> Optional[models.InactiveAlert]: ...
def remove_inactive_alert(inactive_alert: models.InactiveAlert, /) -> None: ...

interview_answers: set[models.InterviewAnswer]

def add_interview_answer(interview_answer: models.InterviewAnswer, /) -> None: ...
def get_interview_answer(id: int, /) -> Optional[models.InterviewAnswer]: ...
def remove_interview_answer(interview_answer: models.InterviewAnswer, /) -> None: ...

interview_configs: set[models.InterviewConfig]

def add_interview_config(interview_config: models.InterviewConfig, /) -> None: ...
def get_interview_config(id: int, /) -> Optional[models.InterviewConfig]: ...
def remove_interview_config(interview_config: models.InterviewConfig, /) -> None: ...

interview_questions: set[models.InterviewQuestion]

def add_interview_question(interview_question: models.InterviewQuestion, /) -> None: ...
def get_interview_question(id: int, /) -> Optional[models.InterviewQuestion]: ...
def remove_interview_question(
    interview_question: models.InterviewQuestion, /
) -> None: ...

interviews: set[models.Interview]

def add_interview(interview: models.Interview, /) -> None: ...
def get_interview(id: int, /) -> Optional[models.Interview]: ...
def remove_interview(interview: models.Interview, /) -> None: ...

mentions: set[models.Mention]

def add_mention(mention: models.Mention, /) -> None: ...
def get_mention(id: int, /) -> Optional[models.Mention]: ...
def remove_mention(mention: models.Mention, /) -> None: ...

menu_interfaces: set[models.MenuInterface]

def add_menu_interface(menu_interface: models.MenuInterface, /) -> None: ...
def get_menu_interface(id: int, /) -> Optional[models.MenuInterface]: ...
def remove_menu_interface(menu_interface: models.MenuInterface, /) -> None: ...

menu_items: set[models.MenuItem]

def add_menu_item(menu_item: models.MenuItem, /) -> None: ...
def get_menu_item(id: int, /) -> Optional[models.MenuItem]: ...
def remove_menu_item(menu_item: models.MenuItem, /) -> None: ...

menus: set[models.Menu]

def add_menu(menu: models.Menu, /) -> None: ...
def get_menu(id: int, /) -> Optional[models.Menu]: ...
def remove_menu(menu: models.Menu, /) -> None: ...

nations: set[models.Nation]

def add_nation(nation: models.Nation, /) -> None: ...
def get_nation(id: int, /) -> Optional[models.Nation]: ...
def remove_nation(nation: models.Nation, /) -> None: ...

nations_private: set[models.NationPrivate]

def add_nation_private(nation_private: models.NationPrivate, /) -> None: ...
def get_nation_private(id: int, /) -> Optional[models.NationPrivate]: ...
def remove_nation_private(nations_private: models.NationPrivate, /) -> None: ...

reminders: set[models.Reminder]

def add_reminder(reminder: models.Reminder, /) -> None: ...
def get_reminder(id: int, /) -> Optional[models.Reminder]: ...
def remove_reminder(reminder: models.Reminder, /) -> None: ...

roles: set[models.Role]

def add_role(role: models.Role, /) -> None: ...
def get_role(id: int, /) -> Optional[models.Role]: ...
def remove_role(role: models.Role, /) -> None: ...

rosters: set[models.Roster]

def add_roster(roster: models.Roster, /) -> None: ...
def get_roster(id: int, /) -> Optional[models.Roster]: ...
def remove_roster(roster: models.Roster, /) -> None: ...

servers: set[models.Server]

def add_server(server: models.Server, /) -> None: ...
def get_server(id: int, /) -> Optional[models.Server]: ...
def remove_server(server: models.Server, /) -> None: ...

server_submissions: set[models.ServerSubmission]

def add_server_submission(server_submission: models.ServerSubmission, /) -> None: ...
def get_server_submission(id: int, /) -> Optional[models.ServerSubmission]: ...
def remove_server_submission(server_submission: models.ServerSubmission, /) -> None: ...

subscriptions: set[models.Subscription]

def add_subscription(subscription: models.Subscription, /) -> None: ...
def get_subscription(id: int, /) -> Optional[models.Subscription]: ...
def remove_subscription(subscription: models.Subscription, /) -> None: ...

tags: set[models.Tag]

def add_tag(tag: models.Tag, /) -> None: ...
def get_tag(id: int, /) -> Optional[models.Tag]: ...
def remove_tag(tag: models.Tag, /) -> None: ...

target_configs: set[models.TargetConfig]

def add_target_config(target_config: models.TargetConfig, /) -> None: ...
def get_target_config(id: int, /) -> Optional[models.TargetConfig]: ...
def remove_target_config(target_config: models.TargetConfig, /) -> None: ...

target_raters: set[models.TargetRater]

def add_target_rater(target_rater: models.TargetRater, /) -> None: ...
def get_target_rater(id: int, /) -> Optional[models.TargetRater]: ...
def remove_target_rater(target_rater: models.TargetRater, /) -> None: ...

target_reminders: set[models.TargetReminder]

def add_target_reminder(target_reminder: models.TargetReminder, /) -> None: ...
def get_target_reminder(id: int, /) -> Optional[models.TargetReminder]: ...
def remove_target_reminder(target_reminder: models.TargetReminder, /) -> None: ...

tax_brackets: set[models.TaxBracket]

def add_tax_bracket(tax_bracket: models.TaxBracket, /) -> None: ...
def get_tax_bracket(id: int, /) -> Optional[models.TaxBracket]: ...
def remove_tax_bracket(tax_bracket: models.TaxBracket, /) -> None: ...

ticket_configs: set[models.TicketConfig]

def add_ticket_config(ticket_config: models.TicketConfig, /) -> None: ...
def get_ticket_config(id: int, /) -> Optional[models.TicketConfig]: ...
def remove_ticket_config(ticket_config: models.TicketConfig, /) -> None: ...

tickets: set[models.Ticket]

def add_ticket(ticket: models.Ticket, /) -> None: ...
def get_ticket(id: int, /) -> Optional[models.Ticket]: ...
def remove_ticket(ticket: models.Ticket, /) -> None: ...

trades: set[models.Trade]

def add_trade(trade: models.Trade, /) -> None: ...
def get_trade(id: int, /) -> Optional[models.Trade]: ...
def remove_trade(trade: models.Trade, /) -> None: ...

transactions: set[models.Transaction]

def add_transaction(transaction: models.Transaction, /) -> None: ...
def get_transaction(id: int, /) -> Optional[models.Transaction]: ...
def remove_transaction(transaction: models.Transaction, /) -> None: ...

treasures: set[models.Treasure]

def add_treasure(treasure: models.Treasure, /) -> None: ...
def get_treasure(name: str, /) -> Optional[models.Treasure]: ...
def remove_treasure(treasure: models.Treasure, /) -> None: ...

treaties: set[models.Treaty]

def add_treaty(treaty: models.Treaty, /) -> None: ...
def get_treaty(id: int, /) -> Optional[models.Treaty]: ...
def remove_treaty(treaty: models.Treaty, /) -> None: ...

users: set[models.User]

def add_user(user: models.User, /) -> None: ...
def get_user(id: int, /) -> Optional[models.User]: ...
def remove_user(user: models.User, /) -> None: ...

war_attacks: set[models.WarAttack]

def add_war_attack(war_attack: models.WarAttack, /) -> None: ...
def get_war_attack(id: int, /) -> Optional[models.WarAttack]: ...
def remove_war_attack(war_attack: models.WarAttack, /) -> None: ...

war_room_configs: set[models.WarRoomConfig]

def add_war_room_config(war_room_config: models.WarRoomConfig, /) -> None: ...
def get_war_room_config(id: int, /) -> Optional[models.WarRoomConfig]: ...
def remove_war_room_config(war_room_config: models.WarRoomConfig, /) -> None: ...

war_rooms: set[models.WarRoom]

def add_war_room(war_room: models.WarRoom, /) -> None: ...
def get_war_room(id: int, /) -> Optional[models.WarRoom]: ...
def remove_war_room(war_room: models.WarRoom, /) -> None: ...

wars: set[models.War]

def add_war(war: models.War, /) -> None: ...
def get_war(id: int, /) -> Optional[models.War]: ...
def remove_war(war: models.War, /) -> None: ...
