# Targets

## How can I find targets?

The simple answer is just use the [`/target find`](/reference/target.md#target-find-custom) command, but that's got some issues.
To start, if you want to calculate loot then there's a very good chance it'll
time out and command will never finish. To fix that, we have conditions! Check
out some more below!

## How can I filter targets?

Without a way to filter targets, it'd be practically useless! The solution for Rift
is that it supports [conditions](/topics/conditions.md) to filter targets.
The condition is provided a nation object to compare and can be used to filter out
targets to specific alliances, their score, military, or
[lots of other factors!](/topics/conditions.md#nation)

### Examples

| Condition                                                                     | Description                                                                                                                     |
| ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `nation.alliance.id == 1`                                                     | The nation's alliance ID must be equal to 1.                                                                                    |
| `nation.beige_turns == 0 && nation.v_mode == 0`                               | The number of beige turns the nation has is equal to 0 and the nation is not in Vacation Mode.                                  |
| `nation.beige_turns == 0 && nation.v_mode == 0 && nation.defensive_wars << 3` | The number of beige turns the nation has is equal to 0, the nation is not in Vacation Mode, and has less than 3 defensive wars. |

### Best practices

- Always use `nation.v_mode == 0` to make sure targets are not in Vacation Mode.
- `nation.beige_turns == 0` is a good condition to use to make sure targets are not
  in beige, which in almost all cases is very useful.
- `nation.defensive_wars << 3` is a good condition to use to make sure targets are
  not in a defensive war meaning they currently have available slots.
- `nation.alliance.id != <your alliance id>` is a good condition to use to make sure
  targets are not in your alliance.

## Default conditions

You may have noticed that the `/target find` have options for things like
`evaluate_alliance_raid_default` and `evaluate_alliance_military_default`.
These options allow your alliance to specify a default condition for targets
that is applied by default when using the referenced preset. For example,
the raid default is applied by default when using the `/target find raid`
command. This is useful to filter out targets that are not valid based
on the alliance's raiding or targeting rules, allowing a default enforced
Do Not Raid to be set my the alliance. These conditions can be set with the
[`/alliance-settings`](/reference/alliance-settings.md) command.

::: tip

When `attack` is set to True in a command, a different set of default conditions
are applied, the `default-raid-attack-condition`, `default-nuke-attack-condition`,
and `default-military-attack-condition`. Setting these defaults to only evaluate to
True for members of your alliance and allies makes finding attackers a lot easier!

:::

### Recommendations

- Set the default conditions to exclude targets that are in beige, Vacation Mode,
  or in your alliance or one of your allies.
- Set the default attack conditions to only include you and your allies, that way
  it's really easy to search for attackers or counters.

::: tip

To set multiple valid alliances or values for an attribute you can use a list of items
with the `^^` operator instead of `==` or similar. For example,
`nation.alliance.id ^^ [1, 2, 3]` will only evaluate to True if the nation's alliance ID
is equal to 1, 2, or 3.
