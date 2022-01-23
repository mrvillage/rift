# `/menu`

The menu command group provides information and utilities
related to custom menus.

## `/menu list`

Lists all the menus in the server

## `/menu create`

Initiates a new menu creation session, ended by typing `finish`, `cancel`,
`complete`, `done`, `save`, or `stop`.

### Parameters

- `description` : The description of the menu, will be displayed when it is posted.

## `/menu edit`

Initiates a new menu creation session to override the menu specified.

### Parameters

- `description` : The new description of the menu, will be displayed when it is posted.

## `/menu send`

Sends a menu to the specified channel.

### Parameters

- `menu` : {{ $var.menuArgument }}
- `channel` : The channel to send the menu to.

## `/menu info`

Displays information about the specified menu.

### Parameters

- `menu` : {{ $var.menuArgument }}

## `/menu item`

- `item` : {{ $var.menuItemArgument }}
