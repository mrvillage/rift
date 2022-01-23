# Subscriptions

## What are subscriptions?

Subscriptions are a super powerful feature that allow you to get near realtime
updates when things change in the game!

## Why are subscriptions useful?

Subscriptions are useful for everything from keeping on top of treaty changes and
new alliances, to knowing when a new nation joins your alliance and when
someone heads out to Vacation Mode for a while!

## How can I subscribe to an event?

Check out the [`/subscribe` command](/reference/subscribe.md) for the
various event commands! Currently, Rift supports the following events:

- `NATION_CREATE`
- `NATION_DELETE`
- `NATION_UPDATE`
- `ALLIANCE_CREATE`
- `ALLIANCE_DELETE`,
- `TREATY_CREATE`
- `TREATY_DELETE`
- `WAR_CREATE`
- `FORUM_POST_CREATE`

## How can I filter events?

Obviously if you subscribe to an event raw you'll get a _lot_ of events, so of
course there's a way to filter them! All `NATION`, `ALLIANCE`, and `WAR` events
support `condition` arguments using Rift's [conditions](/topics/conditions.md) to
determine what events will be sent. If the condition evaluates to True, then it
is sent, otherwise the event is ignored.
The root object of `NATION` and `WAR` events is a [nation](/topics/conditions.md#nation)
and the root object of `ALLIANCE` events is an [alliance](/topics/conditions.md#alliance).
