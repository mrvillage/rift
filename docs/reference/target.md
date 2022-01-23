# `/target`

The target command group provides utilities related to finding
targets and setting target reminders.

## `/target reminder add`

Adds a target reminder.

### Parameters

- `nation` : {{ $var.nationArgument }}
- `channels` : A space separated list of channels to send the reminder to.
- `mentions` : A space separated list of role or user mentions to mention when
  the reminder is sent.
- `direct_message` : Whether to send the reminder in a direct message as well.

## `/target reminder remove`

Remove a target reminder.

### Parameters

- `reminder` : {{ $var.targetReminderArgument }}

## `/target reminder list`

List all target reminders the user has.

## `/target reminder info`

Get information about a target reminder.

### Parameters

- `reminder` : {{ $var.targetReminderArgument }}

## `/target find custom`

Find war targets with a custom configuration.

### Parameters

- `condition` : {{ $var.targetFindConditionArgument }}
- `nation`: {{ $var.nationArgument }}
- `count_cities` : {{ $var.targetFindCountCitiesArgument }}
  {{ $var.defaultFalseArgument }}
- `count_loot` : {{ $var.targetFindCountLootArgument }}
  {{ $var.defaultFalseArgument }}
- `count_infrastructure` : {{ $var.targetFindCountInfrastructureArgument }}
  {{ $var.defaultFalseArgument }}
- `count_military` : {{ $var.targetFindCountMilitaryArgument }}
  {{ $var.defaultFalseArgument }}
- `count_activity` : {{ $var.targetFindCountActivityArgument }}
  {{ $var.defaultFalseArgument }}
- `evaluate_alliance_raid_default` : {{ $var.
  targetFindEvaluateAllianceRaidDefaultArgument }}
  {{ $var.defaultFalseArgument }}
- `evaluate_alliance_nuke_default` : {{ $var.
  targetFindEvaluateAllianceNukeDefaultArgument }}
  {{ $var.defaultFalseArgument }}
- `eval_alliance_military_default` : {{ $var.
  targetFindEvaluateAllianceMilitaryDefaultArgument }}
  {{ $var.defaultFalseArgument }}
- `offset` : {{ $var.targetFindOffsetArgument }}
- `attack` : {{ $var.targetFindAttackArgument }}

## `/target find raid`

Find war targets with the raid configuration.

### Parameters

- `condition` : {{ $var.targetFindConditionArgument }}
- `nation`: {{ $var.nationArgument }}
- `count_infrastructure` : {{ $var.targetFindCountInfrastructureArgument }}
  {{ $var.defaultFalseArgument }}
- `evaluate_alliance_raid_default` : {{ $var.
  targetFindEvaluateAllianceRaidDefaultArgument }}
  {{ $var.defaultTrueArgument }}
- `offset` : {{ $var.targetFindOffsetArgument }}
- `attack` : {{ $var.targetFindAttackArgument }}

## `/target find nuke`

Find war targets with a the nuke configuration.

### Parameters

- `condition` : {{ $var.targetFindConditionArgument }}
- `nation`: {{ $var.nationArgument }}
- `count_loot` : {{ $var.targetFindCountLootArgument }}
  {{ $var.defaultFalseArgument }}
- `count_military` : {{ $var.targetFindCountMilitaryArgument }}
  {{ $var.defaultFalseArgument }}
- `count_activity` : {{ $var.targetFindCountActivityArgument }}
  {{ $var.defaultFalseArgument }}
- `evaluate_alliance_nuke_default` : {{ $var.
  targetFindEvaluateAllianceNukeDefaultArgument }}
  {{ $var.defaultFalseArgument }}
- `offset` : {{ $var.targetFindOffsetArgument }}
- `attack` : {{ $var.targetFindAttackArgument }}

## `/target find military`

Find war targets with a the military configuration.

### Parameters

- `condition` : {{ $var.targetFindConditionArgument }}
- `nation`: {{ $var.nationArgument }}
- `count_cities` : {{ $var.targetFindCountCitiesArgument }}
  {{ $var.defaultFalseArgument }}
- `count_loot` : {{ $var.targetFindCountLootArgument }}
  {{ $var.defaultFalseArgument }}
- `count_infrastructure` : {{ $var.targetFindCountInfrastructureArgument }}
  {{ $var.defaultFalseArgument }}
- `count_activity` : {{ $var.targetFindCountActivityArgument }}
  {{ $var.defaultFalseArgument }}
- `eval_alliance_military_default` : {{ $var.
  targetFindEvaluateAllianceMilitaryDefaultArgument }}
  {{ $var.defaultFalseArgument }}
- `offset` : {{ $var.targetFindOffsetArgument }}
- `attack` : {{ $var.targetFindAttackArgument }}
