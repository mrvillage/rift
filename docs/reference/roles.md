# `/roles`

The roles command group provides a set of utilities to create and
manage alliance roles.

## `/roles create`

Create an alliance role in the designated alliance and open a
select menu to set the permissions.

### Parameters

- `name` : {{ $var.rolesNameArgument }}
- `rank` : {{ $var.rolesRankArgument }}
- `starting_members` : A space separated list of users to add to the role upon creation.
- `description` : {{ $var.rolesDescriptionArgument }}
- `alliance` : {{ $var.allianceArgument }}
- `privacy_level` : {{ $var.rolesPrivacyLevelArgument }}

## `/roles delete`

Delete an alliance role.

### Parameters

- `role` : {{ $var.rolesRoleArgument }}

## `/roles list`

List the roles you can see of an alliance.

### Parameters

- `alliance` : {{ $var.allianceArgument }}

## `/roles info`

Display information about a role.

### Parameters

- `role` : {{ $var.rolesRoleArgument }}

## `/roles edit`

Edit an alliance role.

### Parameters

- `role` : {{ $var.rolesRoleArgument }}
- `name` : {{ $var.rolesNameArgument }}
- `rank` : {{ $var.rolesRankArgument }}
- `description`: {{ $var.rolesDescriptionArgument }}
- `privacy_level` : {{ $var.rolesPrivacyLevelArgument }}

## `/roles add-member`

Adds a member to an alliance role.

### Parameters

- `role` : {{ $var.rolesRoleArgument }}
- `member` : {{ $var.memberOrUserArgument }}

## `/roles remove-member`

Removes a member from an alliance role.

### Parameters

- `role` : {{ $var.rolesRoleArgument }}
- `member` : {{ $var.memberOrUserArgument }}

## `/roles summary`

Show a summary of a user's roles and permissions in an alliance.

### Parameters

- `member` : {{ $var.memberOrUserArgument }}
- `alliance` : {{ $var.allianceArgument }}
