# `/subscribe`

The subscribe command group provides a set of utilities
for subscribing to events.

## `/subscribe nation create`

Subscribe to `NATION_CREATE` events in the current channel.
The provided condition determines if the event should be
broadcast or not.

### Parameters

- `condition` : {{ $var.conditionArgument }}

## `/subscribe nation delete`

Subscribe to `NATION_DELETE` events in the current channel.
The provided condition determines if the event should be
broadcast or not.

### Parameters

- `condition` : {{ $var.conditionArgument }}

## `/subscribe nation update`

Subscribe to `NATION_UPDATE` events in the current channel.
The provided condition determines if the event should be
broadcast or not.

### Parameters

- `changes` : A space separated list of changes to broadcast about.
  Valid changes are `ALLIANCE_POSITION`, `ALLIANCE_POSITION_ALL`,
  `ALLIANCE`, and `VACATION_MODE`.
- `condition` : {{ $var.conditionArgument }}

## `/subscribe alliance create`

Subscribe to `ALLIANCE_CREATE` events in the current channel.
The provided condition determines if the event should be
broadcast or not.

### Parameters

- `condition` : {{ $var.conditionArgument }}

## `/subscribe alliance delete`

Subscribe to `ALLIANCE_DELETE` events in the current channel.
The provided condition determines if the event should be
broadcast or not.

### Parameters

- `condition` : {{ $var.conditionArgument }}

## `/subscribe treaty create`

Subscribe to `TREATY_CREATE` events in the current channel.

## `/subscribe treaty delete`

Subscribe to `TREATY_CREATE` events in the current channel.

## `/subscribe forum-post create`

Subscribe to `FORUM_POST_CREATE` events in the current channel.

### Parameters

- `forums` : A space separated list of forums to subscribe to.
  Valid forums are `ALLIANCE_AFFAIRS` and `ORBIS_CENTRAL`.

## `/subscribe war create`

Subscribe to `WAR_CREATE` events in the current channel.
The provided condition determines if the event should be
broadcast or not. The condition will be evaluated against
the nations involved in the war.

### Parameters

- `condition` : {{ $var.conditionArgument }}
