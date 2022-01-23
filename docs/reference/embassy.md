# `/embassy`

The embassy command group provides a set of commands for dealing with embassies.

## `/embassy open`

Open a embassy with the provided configuration.

### Parameters

- `config` : {{ $var.embassyConfigArgument }}

## `/embassy config create`

Creates a embassy configuration.

### Parameters

- `start` : The starting message for when a embassy is created.
- `category` : {{ $var.categoryChannelArgument }}

## `/embassy config list`

List all embassy configurations in the server.

## `/embassy config claim`

Claim an embassy for an alliance in a specific embassy configuration.

### Parameters

- `config` : {{ $var.embassyConfigArgument }}
- `alliance` : {{ $var.allianceArgument }}
- `channel` : {{ $var.textChannelArgument }}
  Defaults to the current channel.
