CREATE TABLE "users" (
  "user_id" bigint,
  "nation_id" bigint,
  "uuid" uuid
);

CREATE TABLE "nations" (
  "id" integer,
  "alliance_id" integer,
  "alliance_position" smallint,
  "name" text,
  "leader" text,
  "continent" smallint,
  "war_policy" smallint,
  "domestic_policy" smallint,
  "color" smallint,
  "num_cities" integer,
  "score" numeric,
  "flag" text,
  "vacation_mode_turns" integer,
  "beige_turns" integer,
  "espionage_available" boolean,
  "last_active" timestamp with time zone,
  "date" timestamp with time zone,
  "soldiers" integer,
  "tanks" integer,
  "aircraft" integer,
  "ships" integer,
  "missiles" integer,
  "nukes" integer,
  "discord_username" text,
  "turns_since_last_city" integer,
  "turns_since_last_project" integer,
  "projects" integer,
  "wars_won" integer,
  "wars_lost" integer,
  "tax_id" integer,
  "alliance_seniority" integer,
  "estimated_resources" resources
);

CREATE TABLE "nations_private" (
  "id" integer,
  "update_tz" numeric,
  "spies" integer,
  "resources" resources
);

CREATE TABLE "alliances" (
  "id" integer,
  "name" text,
  "acronym" text,
  "score" numeric,
  "color" smallint,
  "date" timestamp with time zone,
  "accepts_members" boolean,
  "flag" text,
  "forum_link" text,
  "discord_link" text,
  "wiki_link" text,
  "estimated_resources" resources
);

CREATE TABLE "alliances_private" (
  "id" integer,
  "resources" resources
);

CREATE TABLE "cities" (
  "id" integer,
  "nation_id" integer,
  "name" text,
  "date" timestamp with time zone,
  "infrastructure" numeric,
  "land" numeric,
  "powered" boolean,
  "coal_power" integer,
  "oil_power" integer,
  "nuclear_power" integer,
  "wind_power" integer,
  "coal_mines" integer,
  "lead_mines" integer,
  "bauxite_mine" integer,
  "oil_well" integer,
  "uranium_mine" integer,
  "iron_mines" integer,
  "farms" integer,
  "oil_refineries" integer,
  "steel_mills" integer,
  "aluminum_refineries" integer,
  "munitions_factories" integer,
  "police_stations" integer,
  "hospitals" integer,
  "recycling_center" integer,
  "subways" integer,
  "supermarkets" integer,
  "banks" integer,
  "shopping_malls" integer,
  "stadiums" integer,
  "barracks" integer,
  "factories" integer,
  "hangars" integer,
  "drydocks" integer,
  "nuke_date" timestamp with time zone
);

CREATE TABLE "trades" (
  "id" integer,
  "type" smallint,
  "date" timestamp with time zone,
  "sender_id" integer,
  "receiver_id" integer,
  "resource" smallint,
  "amount" integer,
  "action" smallint,
  "price" integer,
  "accepted" boolean,
  "date_accepted" timestamp with time zone,
  "original_trade_id" integer
);

CREATE TABLE "bankrecs" (
  "id" integer,
  "date" timestamp with time zone,
  "sender_id" integer,
  "sender_type" smallint,
  "receiver_id" integer,
  "receiver_type" smallint,
  "banker_id" integer,
  "note" text,
  "resources" resources,
  "tax_id" integer
);

CREATE TABLE "treaties" (
  "id" integer,
  "date" timestamp with time zone,
  "type" smallint,
  "url" text,
  "turns_left" integer,
  "sender_id" integer,
  "receiver_id" integer
);

CREATE TABLE "colors" (
  "date" timestamp with time zone,
  "data" text
);

CREATE TABLE "wars" (
  "id" integer,
  "date" timestamp with time zone,
  "reason" text,
  "type" smallint,
  "attacker_id" integer,
  "attacker_alliance_id" integer,
  "defender_id" integer,
  "defender_alliance_id" integer,
  "ground_control" integer,
  "air_superiority" integer,
  "naval_blockade" integer,
  "winner_id" integer,
  "turns_left" integer,
  "attacker_action_points" integer,
  "defender_action_points" integer,
  "attacker_resistance" integer,
  "defender_resistance" integer,
  "attacker_peace" boolean,
  "defender_peace" boolean,
  "attacker_fortify" boolean,
  "defender_fortify" boolean,
  "attacker_gasoline_used" numeric,
  "defender_gasoline_used" numeric,
  "attacker_munitions_used" numeric,
  "defender_munitions_used" numeric,
  "attacker_aluminum_used" numeric,
  "defender_aluminum_used" numeric,
  "attacker_steel_used" numeric,
  "defender_steel_used" numeric,
  "attacker_infrastructure_destroyed" numeric,
  "defender_infrastructure_destroyed" numeric,
  "attacker_money_looted" numeric,
  "defender_money_looted" numeric,
  "attacker_soldiers_killed" integer,
  "defender_soldiers_killed" integer,
  "attacker_tanks_killed" integer,
  "defender_tanks_killed" integer,
  "attacker_aircraft_killed" integer,
  "defender_aircraft_killed" integer,
  "attacker_ships_killed" integer,
  "defender_ships_killed" integer,
  "attacker_missiles_used" integer,
  "defender_missiles_used" integer,
  "attacker_nukes_used" integer,
  "defender_nukes_used" integer,
  "attacker_infrastructure_destroyed_value" numeric,
  "defender_infrastructure_destroyed_value" numeric
);

CREATE TABLE "war_attacks" (
  "id" integer,
  "date" timestamp with time zone,
  "attacker_id" integer,
  "defender_id" integer,
  "type" smallint,
  "war_id" integer,
  "victor_id" integer,
  "success" integer,
  "attcas1" integer,
  "attcas2" integer,
  "defcas1" integer,
  "defcas2" integer,
  "city_id" integer,
  "infrastructure_destroyed" numeric,
  "improvements_lost" integer,
  "money_stolen" numeric,
  "loot_info" text,
  "resistance_eliminated" integer,
  "city_infrastructure_before" numeric,
  "infrastructure_destroyed_value" numeric,
  "attacker_munitions_used" numeric,
  "defender_munitions_used" numeric,
  "attacker_gasoline_used" numeric,
  "defender_gasoline_used" numeric,
  "aircraft_killed_by_tanks" integer
);

CREATE TABLE "treasures" (
  "date" timestamp with time zone,
  "data" text
);

CREATE TABLE "radiation" (
  "date" timestamp with time zone,
  "data" text
);

CREATE TABLE "bounties" (
  "id" integer,
  "date" timestamp with time zone,
  "nation_id" integer,
  "amount" integer,
  "type" smallint
);

CREATE TABLE "tax_brackets" (
  "id" integer,
  "alliance_id" integer,
  "name" text,
  "date" timestamp with time zone,
  "date_modified" timestamp with time zone,
  "last_modifier_id" integer,
  "tax_rate" integer,
  "resource_tax_rate" integer
);

CREATE TABLE "menus" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "guild_id" bigint,
  "name" text,
  "description" text,
  "layout" integer[][]
);

CREATE TABLE "menu_items" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "menu_id" integer,
  "type" smallint,
  "style" smallint,
  "label" text,
  "disabled" boolean,
  "url" text,
  "emoji" bigint,
  "action" smallint,
  "action_options" integer[]
);

CREATE TABLE "menu_interfaces" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "menu_id" integer,
  "message_id" bigint,
  "channel_id" bigint,
  "guild_id" bigint
);

CREATE TABLE "target_configs" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "owner_id" bigint,
  "name" text,
  "count" bigint,
  "rater" integer,
  "condition" text,
  "use_condition" text,
  "attack" boolean
);

CREATE TABLE "target_raters" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "cities" text,
  "infrastructure" text,
  "activity" text,
  "soldiers" text,
  "tanks" text,
  "aircraft" text,
  "ships" text,
  "missiles" text,
  "nukes" text,
  "money" text,
  "coal" text,
  "oil" text,
  "uranium" text,
  "iron" text,
  "bauxite" text,
  "lead" text,
  "gasoline" text,
  "munitions" text,
  "steel" text,
  "aluminum" text,
  "food" text
);

CREATE TABLE "target_reminders" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "nation_id" integer,
  "owner_id" bigint,
  "mention_ids" integer[],
  "direct_message" boolean,
  "times" integer[]
);

CREATE TABLE "reminders" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "name" text,
  "message" text,
  "owner_id" bigint,
  "mention_ids" integer[],
  "direct_message" boolean,
  "date" timestamp with time zone,
  "interval" interval
);

CREATE TABLE "tags" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "name" text,
  "owner_id" bigint,
  "text" text,
  "use_condition" text
);

CREATE TABLE "roles" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "name" text,
  "description" text,
  "alliance_id" integer,
  "rank" integer,
  "permissions" bigint,
  "member_ids" bigint[],
  "role_ids" bigint[],
  "alliance_positions" integer[],
  "privacy_level" integer,
  "access_level" smallint
);

CREATE TABLE "guild_roles" (
  "id" bigint,
  "guild_id" bigint,
  "permissions" bigint
);

CREATE TABLE "ticket_configs" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "name" text,
  "category_id" bigint,
  "guild_id" bigint,
  "message" text,
  "archive_category_id" bigint,
  "mention_ids" integer[],
  "default" boolean,
  "name_format" text,
  "interview_config_id" integer,
  "close_action" smallint,
  "transcript_channel_id" bigint
);

CREATE TABLE "tickets" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "ticket_number" integer,
  "config_id" integer,
  "guild_id" bigint,
  "channel_id" bigint,
  "owner_id" bigint,
  "closed" boolean
);

CREATE TABLE "embassy_configs" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "name" text,
  "category_id" bigint,
  "guild_id" bigint,
  "message" text,
  "archive_category_id" bigint,
  "mentions" integer[],
  "default" boolean,
  "name_format" text,
  "access_level" smallint
);

CREATE TABLE "embassies" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "config_id" integer,
  "guild_id" bigint,
  "channel_id" bigint,
  "alliance_id" bigint,
  "archived" boolean
);

CREATE TABLE "mentions" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "owner_id" bigint,
  "owner_type" smallint,
  "channel_ids" bigint[],
  "role_ids" bigint[],
  "user_ids" bigint[]
);

CREATE TABLE "alliance_settings" (
  "alliance_id" integer,
  "default_raid_condition" text,
  "default_nuke_condition" text,
  "default_military_condition" text,
  "default_attack_raid_condition" text,
  "default_attack_nuke_condition" text,
  "default_attack_military_condition" text,
  "withdraw_channel_ids" bigint[],
  "require_withdraw_approval" boolean,
  "offshore_id" integer,
  "withdraw_from_offshore" boolean
);

CREATE TABLE "guild_settings" (
  "guild_id" bigint,
  "purpose" smallint,
  "purpose_argument" text,
  "public" boolean,
  "description" text,
  "welcome_message" text,
  "welcome_channels" bigint[],
  "join_role_ids" bigint[],
  "verified_role_ids" bigint[],
  "member_role_ids" bigint[],
  "verified_nickname_format" text,
  "enforce_verified_nickname" boolean,
  "welcome_mentions" integer[]
);

CREATE TABLE "alliance_auto_roles" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "role_id" bigint,
  "guild_id" bigint,
  "alliance_id" integer,
  "access_level" smallint,
  "condition" text
);

CREATE TABLE "city_auto_roles" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "role_id" bigint,
  "guild_id" bigint,
  "min_city" integer,
  "max_city" integer,
  "members_only" boolean,
  "condition" text
);

CREATE TABLE "conditional_auto_roles" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "role_id" bigint,
  "guild_id" bigint,
  "condition" text
);

CREATE TABLE "conditions" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "name" text,
  "owner_id" bigint,
  "value" text,
  "use_condition" text
);

CREATE TABLE "webhooks" (
  "id" bigint,
  "channel_id" bigint,
  "guild_id" bigint,
  "token" text
);

CREATE TABLE "subscriptions" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "guild_id" bigint,
  "channel_id" bigint,
  "owner_id" bigint,
  "event" text,
  "sub_types" text[],
  "condition" text,
  "mentions" integer[]
);

CREATE TABLE "accounts" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "name" text,
  "owner_id" bigint,
  "alliance_id" integer,
  "resources" resources,
  "war_chest" boolean,
  "primary" boolean,
  "deposit_code" text
);

CREATE TABLE "transactions" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "date" timestamp with time zone,
  "status" smallint,
  "type" smallint,
  "creator_id" bigint,
  "to_id" bigint,
  "to_type" smallint,
  "from_id" bigint,
  "from_type" smallint,
  "resources" resources,
  "note" text
);

CREATE TABLE "grants" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "date" timestamp with time zone,
  "status" smallint,
  "recipient" bigint,
  "resources" resources,
  "alliance_id" integer,
  "note" text,
  "payoff_type" smallint,
  "deadline" timestamp with time zone,
  "expiry" timestamp with time zone,
  "paid" resources,
  "payoff_code" text,
  "tax_bracket" integer
);

CREATE TABLE "war_room_configs" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "name" text,
  "channel_id" bigint,
  "category_ids" bigint[],
  "guild_id" bigint,
  "message" text,
  "mention_ids" integer[],
  "name_format" text,
  "reuse" boolean,
  "condition" text,
  "track_wars" boolean,
  "advise" boolean
);

CREATE TABLE "war_rooms" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "config_id" integer,
  "guild_id" bigint,
  "channel_id" bigint,
  "nation_id" integer,
  "war_ids" bigint[],
  "archived" boolean,
  "thread" boolean
);

CREATE TABLE "blitzes" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "date" timestamp with time zone,
  "name" text,
  "message" text,
  "alliance_ids" integer[],
  "planning_alliance_ids" integer[],
  "war_room_config" integer,
  "direct_message" boolean,
  "in_game_message" boolean
);

CREATE TABLE "blitz_targets" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "blitz_id" integer,
  "war_room_id" integer,
  "nation_id" integer,
  "attacker_ids" integer[]
);

CREATE TABLE "inactive_alerts" (
  "nation_id" integer,
  "last_alert" timestamp with time zone
);

CREATE TABLE "audit_configs" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "name" text,
  "alliance_id" integer,
  "fail_message_format" text,
  "success_message_format" text
);

CREATE TABLE "audit_checks" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "name" text,
  "config_id" integer,
  "condition" text,
  "fail_message_format" text,
  "success_message_format" text,
  "required" boolean,
  "city" boolean
);

CREATE TABLE "audit_runs" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "config_id" integer,
  "nation_id" integer,
  "checks" json
);

CREATE TABLE "interview_configs" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "name" text,
  "guild_id" bigint
);

CREATE TABLE "interviews" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "config_id" integer,
  "owner_id" bigint,
  "ticket_id" integer,
  "require_link" boolean
);

CREATE TABLE "interview_questions" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "name" text,
  "config_id" integer,
  "question" text,
  "position" integer,
  "answer_type" smallint,
  "choices" text[],
  "min_choices" integer,
  "max_choices" integer
);

CREATE TABLE "interview_answers" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "question_id" integer,
  "interview_id" integer,
  "answer" text
);

CREATE TABLE "audit_logs" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "config_id" integer,
  "guild_id" bigint,
  "channel_id" bigint,
  "user_id" bigint,
  "alliance_id" integer,
  "action" smallint,
  "data" json
);

CREATE TABLE "audit_log_configs" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "guild_id" bigint,
  "channel_id" bigint,
  "target_guild_id" bigint,
  "target_alliance_id" integer,
  "actions" smallint[]
);

CREATE TABLE "servers" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "guild_id" bigint,
  "name" text,
  "invite" text,
  "description" text,
  "tags" text[]
);

CREATE TABLE "server_submissions" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "name" text,
  "invite" text,
  "description" text,
  "tags" text[]
);

CREATE TABLE "builds" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "name" text,
  "owner_id" bigint,
  "use_condition" text,
  "infrastructure" numeric,
  "land" numeric,
  "coal_power" integer,
  "oil_power" integer,
  "nuclear_power" integer,
  "wind_power" integer,
  "coal_mines" integer,
  "lead_mines" integer,
  "bauxite_mine" integer,
  "oil_well" integer,
  "uranium_mine" integer,
  "iron_mines" integer,
  "farms" integer,
  "oil_refineries" integer,
  "steel_mills" integer,
  "aluminum_refineries" integer,
  "munitions_factories" integer,
  "police_stations" integer,
  "hospitals" integer,
  "recycling_center" integer,
  "subways" integer,
  "supermarkets" integer,
  "banks" integer,
  "shopping_malls" integer,
  "stadiums" integer,
  "barracks" integer,
  "factories" integer,
  "hangars" integer,
  "drydocks" integer
);

CREATE TABLE "rosters" (
  "id" integer GENERATED BY DEFAULT AS IDENTITY,
  "nation_id" integer,
  "alliance_id" integer,
  "join_date" timestamp with time zone,
  "time_zone" numeric
);

CREATE TABLE "credentials" (
  "nation_id" integer,
  "api_key" text
);

COMMENT ON COLUMN "target_configs"."count" IS 'flags that show what can contain';

COMMENT ON COLUMN "target_configs"."condition" IS 'condition to apply by default when using the config';

COMMENT ON COLUMN "target_configs"."use_condition" IS 'condition to determine who can use the config';

COMMENT ON TABLE "target_raters" IS 'columns will contain an expression to evaluate and will return the rating';

COMMENT ON COLUMN "target_reminders"."times" IS 'array of times (in seconds) to send a reminder before the target leaves beige, will always send a reminder when they do';

COMMENT ON COLUMN "reminders"."interval" IS 'time in seconds to loop the reminder, starting at time, time will be updated to be the next time to remind';

COMMENT ON COLUMN "tags"."use_condition" IS 'condition to determine who can use the tag';

COMMENT ON COLUMN "roles"."access_level" IS 'enum with some values for access level (general, low FA, standard FA, high FA, leadership, etc)';

COMMENT ON COLUMN "ticket_configs"."mention_ids" IS 'will ignore channels in mention config';

COMMENT ON COLUMN "embassy_configs"."mentions" IS 'will ignore channels in mention config';

COMMENT ON TABLE "mentions" IS 'will store mention configurations that can be configured by a user or internally for use by Rift, is useful for simplifying mentions and storage for things like tickets, embassies, and reminders';

COMMENT ON COLUMN "mentions"."owner_type" IS 'enum of owner types that correspond to the owner_id, things like users, embassy configs, ticket configs, etc';

COMMENT ON COLUMN "city_auto_roles"."members_only" IS 'if true, will only give the role to alliance members of the alliance the guild is linked too';

COMMENT ON COLUMN "conditions"."use_condition" IS 'condition to determine who can use the condition';

COMMENT ON COLUMN "subscriptions"."owner_id" IS 'if channel_id is null, owner_id will be the user ID of the user to DM the events too';

COMMENT ON COLUMN "subscriptions"."mentions" IS 'will ignore channels in mention config';

COMMENT ON COLUMN "war_room_configs"."channel_id" IS 'if war rooms are done in threads';

COMMENT ON COLUMN "war_room_configs"."category_ids" IS 'if war rooms are done in categories';

COMMENT ON COLUMN "war_room_configs"."mention_ids" IS 'will ignore channels in mention config';

COMMENT ON COLUMN "war_room_configs"."reuse" IS 'whether to reuse war rooms, if set to false will archive old threads/delete old channels when all wars expire';

COMMENT ON COLUMN "war_room_configs"."condition" IS 'determines whether a user can be added to a war room';

COMMENT ON COLUMN "war_room_configs"."track_wars" IS 'whether to track all wars in the war room with war/attack event cards';

COMMENT ON COLUMN "war_room_configs"."advise" IS 'whether to provide war advise on how to proceed';

COMMENT ON COLUMN "blitzes"."date" IS 'the time the blitz will happen';

COMMENT ON COLUMN "blitzes"."alliance_ids" IS 'the alliances that are blizing';

COMMENT ON COLUMN "blitzes"."planning_alliance_ids" IS 'the alliances planning the blitz, are allowed to edit and view it';

COMMENT ON COLUMN "blitzes"."war_room_config" IS 'the war room config to make war rooms in';

COMMENT ON COLUMN "blitz_targets"."nation_id" IS 'the id of the target nation';

COMMENT ON COLUMN "blitz_targets"."attacker_ids" IS 'the nation IDs of the attacking nations';

COMMENT ON COLUMN "inactive_alerts"."last_alert" IS 'will be used to store the last time an alert was sent, ensures that alerts arent repeated every time data updates';

COMMENT ON COLUMN "audit_checks"."city" IS 'whether to apply the check to each of the nations cities instead of the nation itself';

COMMENT ON COLUMN "audit_runs"."checks" IS 'map of check ID to success boolean';

COMMENT ON COLUMN "interview_questions"."answer_type" IS 'enum of all types, will be short text, long text, and choice';

COMMENT ON COLUMN "rosters"."time_zone" IS 'stored as X in UTC+X, can be negative (UTC-X)';
