# Menus

## What's a menu?

A menu is a series of buttons (and soon select menus!) that can be customized
and used to perform a variety of different actions in a Discord channel.

## What can I do with a menu?

Menus allow you to add custom buttons that do a variety of actions. Currently,
buttons support the following actions:

- `ADD_ROLE`/`ADD_ROLES`
- `REMOVE_ROLE`/`REMOVE_ROLES`
- `TOGGLE_ROLE`/`TOGGLE_ROLES`
- `CREATE_TICKET`/`CREATE_TICKETS`
- `CREATE_EMBASSY`/`CREATE_EMBASSIES`

## How do I make a menu?

Check out the tutorial on making a menu [here](/guilds/my-first-menu.md)!

## How do I add buttons to a menu?

When creating a menu you need to send a series of followup messages containing
menu item information. Currently, the only supported menu item type is a
button.

## How do I specify a menu item?

Menu items are specified with flags, each followup message starts with the
type of item (currently only button) then a bunch of flags, with a name then
a colon, then the value of that flag. For example:
`button label: This is a label style: green action: CREATE_TICKET options: 1 2 3`

## Button flags

- `style`/`color` : The style of button to display, determines the color. Can be
  one of the following:
  - `primary`/`blurple` : Colors the button blurple.
  - `secondary`/`gray`/`grey` : Colors the button gray.
  - `success`/`green` : Colors the button green.
  - `danger`/`red` : Colors the button red.
- `action` : The action to perform on button press, based on the `options`
  flag provided. The action can be one of the following:
  - `ADD_ROLE`/`ADD_ROLES` : Adds the specified role(s) to the user.
    Expects `options` to be space separated role mentions, IDs, or names.
  - `REMOVE_ROLE`/`REMOVE_ROLES` : Removes the specified role(s) from the user.
    Expects `options` to be space separated role mentions, IDs, or names.
  - `TOGGLE_ROLE`/`TOGGLE_ROLES` : Toggles the specified role(s) on the user.
    Expects `options` to be space separated role mentions, IDs, or names.
  - `CREATE_TICKET`/`CREATE_TICKETS` : Creates a ticket for the user.
    Expects `options` to be a space separated list of ticket config IDs.
  - `CREATE_EMBASSY`/`CREATE_EMBASSIES` : Creates an embassy for the user.
    Expects `options` to be a space separated list of embassy config IDs.
- `url` : The URL to redirect to when the button is pressed, can only be
  combined with the `label` and `emoji` flags.
- `label` : The label to display on the button.
- `emoji` : The emoji to display on the button.
- `row` : The row to place the button in, can be any number between 1 and 5.
- `id` : The ID of an existing menu item button to add to the menu.
- `disabled` : Whether or not the button is disabled.
