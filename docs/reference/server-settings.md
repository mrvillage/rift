# `/server-settings`

The server-settings command group provides access to various
settings to configure Rift for the current server

## `/server-settings purpose`

Set or view the server purpose.

### Parameters

- `purpose` : Choose the server purpose. Can be one of `ALLIANCE`,
  `ALLIANCE_GOVERNMENT`, `ALLIANCE_MILITARY_AFFAIRS`,
  `ALLIANCE_INTERNAL_AFFAIRS`, `ALLIANCE_MILITARY_AFFAIRS`,
  `ALLIANCE_FOREIGN_AFFAIRS`, `ALLIANCE_ECONOMIC_AFFAIRS`,
  `BUSINESS`, `COMMUNITY`, or `PERSONAL`.

## `/server-settings welcome-message`

Set or view the server welcome message.

### Parameters

- `message` : The server welcome message.

## `/server-settings verified-nickname`

Set or view the verified nickname format.

### Parameters

- `nickname` : The verified nickname format.

## `/server-settings welcome-channels`

Set or view the welcome channels.

### Parameters

- `channels` : {{ $var.textChannelsArgument }}
- `clear` : {{ $var.clearArgument }} {{ $var.defaultFalseArgument }}

## `/server-settings join-roles`

Set or view the join roles.

### Parameters

- `roles` : {{ $var.rolesArgument }}
- `clear` : {{ $var.clearArgument }} {{ $var.defaultFalseArgument }}

## `/server-settings verified-roles`

Set or view the verified roles.

### Parameters

- `roles` : {{ $var.rolesArgument }}
- `clear` : {{ $var.clearArgument }} {{ $var.defaultFalseArgument }}

## `/server-settings member-roles`

Set or view the roles for members of the same alliance as the server.

### Parameters

- `roles` : {{ $var.rolesArgument }}
- `clear` : {{ $var.clearArgument }} {{ $var.defaultFalseArgument }}

## `/server-settings diplomat-roles`

Set or view the diplomat roles.

### Parameters

- `roles` : {{ $var.rolesArgument }}
- `clear` : {{ $var.clearArgument }} {{ $var.defaultFalseArgument }}

## `/server-settings enforce-verified-nickname`

Set or view whether verified nickname is enforced upon nickname changes.

### Parameters

- `enforce` : Whether or not to enforce the verified nickname
  format on members.

## `/server-settings managers`

Set or view the server manager roles.

### Parameters

- `roles` : {{ $var.rolesArgument }}
- `clear` : {{ $var.clearArgument }} {{ $var.defaultFalseArgument }}

## `/server-settings alliance-auto-roles info`

Show information about the current alliance auto roles configuration.

## `/server-settings alliance-auto-roles toggle`

Toggle alliance auto roles on and off.

### Parameters

- `enable` : Whether or not to enable alliance auto roles.

## `/server-settings alliance-auto-roles toggle-create`

Toggle alliance auto roles automatic role creation on and off.

### Parameters

- `enable` : Whether or not to enable alliance auto roles
  automatic
  role creation.

## `/server-settings alliance-auto-roles list`

List all alliance auto roles.

## `/server-settings alliance-auto-roles add`

Add an auto role to an alliance.

### Parameters

- `role` : {{ $var.roleArgument }}
- `alliance` : {{ $var.allianceArgument }}

## `/server-settings alliance-auto-roles remove`

Remove an auto role from an alliance.

### Parameters

- `role` : {{ $var.roleArgument }}
- `alliance` : {{ $var.allianceArgument }}

## `/server-settings alliance-auto-roles run`

Check and add/remove alliance auto roles from members.
