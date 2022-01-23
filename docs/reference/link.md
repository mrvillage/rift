# `/link`

The link command provides the method by which to link a nation to a user.
Links allow Rift to infer the current user's nation or
alliance for permissions and default values.

## Parameters

- `nation` : {{ $page.global.nationArgumentNoLink }}
- `user` : The user to try linking the nation to.
  Defaults to the user executing the command.

## Special Instructions

When using the `/link` command, be sure that the user's
Discord name and discriminator is in the
[Discord Username section of the nation edit page](https://politicsandwar.com/nation/edit/#discord).
If it is not, then Rift cannot verify that the nation belongs to the user.
