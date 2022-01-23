# Conditions

::: warning
Condition syntax WILL be subject to change and enhancement in the near future,
namely conditions will be migrating to [Common Expression Language](https://github.com/google/cel-spec)
as soon as a performant implementation can be put in place (currently, testing
takes 0.2ms for a simple condition, with an experimental CEL implementation
it took 0.13s, or 130ms to evaluate).
:::

## What are conditions?

Conditions are an incredibly powerful tool allowing users to define
custom conditions to determine whether or not a particular action should
happen or not.
Conditions are essentially a simple boolean expression (meaning something
that is either evaluated by Rift to either be True or False).
Something like `nation.alliance.id == 1` will evaluate to True if the
nation provided is in the alliance with ID 1.

## How can I use conditions?

You can use conditions in lots of places! They've become a foundational
piece of Rift's functionality, and will get even more use in the future.
For example, conditions are used to help filter out targets when using the
[`/target find`](/reference/target-find.md) command or to determine whether
or not to send an event in a subscription.

## How do I use conditions?

You can think of conditions a little bit like English, or math. If you have
basic programming knowledge already you'll have no trouble with this at all!
At present, conditions only apply to nations and alliances, so the root "object"
you'll be comparing to is either called nation or alliance.
From there, you can assemble the rest of the condition based on whatever
criteria your heart desires.
For example, `nation.alliance.id == 1 && nation.alliance_position == "Leader"`
will take the nation given, and check if the nation's alliance's ID is equal to 1
_and_ if the nation's alliance position is equal to "Leader". (The periods denote
an attribute or part of another object, so in this case nation.alliance is an attribute
of nation that gives another object, this time an alliance.)

## Syntax

Conditions follow the following syntax:
`expression | boolean operator | conditional statement | ...`
Expressions are defined as:
`attribute | comparison operator | value`
Expressions can also be conditions themselves if surrounded by parentheses (`(condition)`).
THis syntax can repeat as many times as you'd like.

### Boolean operators

Boolean operators are used to combine multiple expressions. If an and operator
is True, the condition is True if the expressions on both sides of the operator
are True.

- `&&` : And - True if both expressions are True
- `??` : Or - True if either expression is True

## Comparison operators

Comparison operators are used to compare an attribute to a value.
If the attribute meets the comparison for the value, then the expression
evaluates to True.

- `==` : Equal - True if the attribute is equal to the value
- `!=` : Not equal - True if the attribute is not equal to the value
- `>>` : Greater than - True if the attribute is greater than the value
- `<<` : Less than - True if the attribute is less than the value
- `>=` : Greater than or equal to - True if the attribute is greater than or
  equal to the value
- `<=` : Less than or equal to - True if the attribute is less than or
  equal to the value
- `^^` : Contains - True if the value contains the attribute

::: tip
To use the contains operator, define a list of values with brackets
(`[value, value, value]`). If any of the values in your list match
the attribute, the expression evaluates to True.
Example: `nation.alliance.id ^^ [1, 2, 3]`
:::

## Examples

| Condition                                                                                                              | Description                                                                                                                                                                                                                                   |
| ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| nation.alliance.id == 1 && nation.alliance_position >= "Member" && (nation.score >= 3000 ?? nation.soldiers <= 100000) | The nation's alliance ID must be equal to 1 and the nation's alliance position must be greater than or equal to Member and either the nation's score must be greater than 3000 or the nation's soldiers must be less than or equal to 100000. | nation.v_mode == 0 && nation.beige_turns == 0 && nation.defensive_wars << 3 |  |
| alliance.rank <= 50 && alliance.member_count >= 10 && alliance.member_count <= 20                                      | The alliance's rank must be less than or equal to 50 and the alliance's member account must be greater than 10 and the alliance's member count must be less than 20.                                                                          |

## Objects

The following define all the attributes available on the objects passed into conditions.

### `nation`

- `id` : number - The nation's ID
- `alliance` : alliance - The nation's [alliance](#alliance), can get further
  attributes with a `.` then the attribute name, see [alliance](#alliance) below
  for attributes; this attribute does nothing on it's own, another must be used
  with the `.`
- `alliance_position` : text or number - The nation's alliance position, can be
  any of the following names of IDs:
  - None - 0
  - Applicant - 1
  - Member - 2
  - Officer - 3
  - Heir - 4
  - Leader - 5
- `name` : text or number - The nation's name
- `v_mode` : text or number - Whether the nation is on vacation mode (1 or "True"
  for on vacation mode, 0 or "False" for not)
- `v_mode_turns` : number - The number of turns left on the nation's vacation mode
- `war_policy` : text or number - The nation's war policy, can be any of the
  following names of IDs:
  - Attrition - 1
  - Turtle - 2
  - Blitzkrieg - 3
  - Fortress - 4
  - Moneybags - 5
  - Pirate - 6
  - Tactician - 7
  - Guardian - 8
  - Covert - 9
  - Arcane - 10
- `domestic_policy` : text or number - The nation's domestic policy, can be any
  of the following names or IDs:
  - Manifest Destiny - 1
  - Open Markets - 2
  - Technological Advancement - 3
  - Imperialism - 4
  - Urbanization - 5
- `color` : text or number - The nation's color bloc, can be any of the
  following names or IDs:
  - Beige - 0
  - Gray - 1
  - Lime - 2
  - Green - 3
  - White - 4
  - Brown - 5
  - Maroon - 6
  - Purple - 7
  - Blue - 8
  - Red - 9
  - Orange - 10
  - Olive - 11
  - Aqua - 12
  - Black - 13
  - Yellow - 14
  - Pink - 15
- `beige_turns` : number - The number of turns the nation has left on beige
- `score` : number - The nation's score
- `soldiers` : number - The nation's soldiers
- `tanks` : number - The nation's tanks
- `aircraft` : number - The nation's aircraft
- `ships` : number - The nation's ships
- `missiles` : number - The nation's missiles
- `nukes` : number - The nation's nukes
- `defensive_wars` : number - The number of defensive wars the nation is in
- `offensive_wars` : number - The number of offensive wars the nation is in
- `last_active` : text - The nation's last active date, is a string in the format
  `YYYY-MM-DD HH:MM:SS`
- `founded` : text - The nation's founding date, is a string in the format
  `YYYY-MM-DD HH:MM:SS`

### `alliance`

- `id` : number - The alliance's ID
- `member_count` : number - The number of members in the alliance
- `name` : text - The alliance's name
- `rank` : text - The alliance's rank, can be any of the following names
- `score` : number - The alliance's score
