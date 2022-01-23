# `/ticket`

The ticket command group provides a set of commands for dealing with tickets.

## `/ticket archive`

Archive a ticket.

### Parameters

- `channel` : {{ $var.textChannelArgument }}

## `/ticket open`

Open a ticket with the provided configuration.

### Parameters

- `config` : {{ $var.ticketConfigArgument }}

## `/ticket config create`

Creates a ticket configuration.

### Parameters

- `start` : The starting message for when a ticket is created.
- `category` : {{ $var.categoryChannelArgument }}
- `archive_category` : {{ $var.categoryChannelArgument }}
- `mentions` : A space separated list of user and roles
  to mention when a ticket is created.

## `/ticket config list`

List all ticket configurations in the server.
