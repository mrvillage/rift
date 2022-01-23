# `/subscription`

The subscription command group provides a set of utilities
to manage subscriptions.

## `/subscription list`

List all the subscriptions in the server or the provided channel.

### Parameters

- `channel` : {{ $var.textChannelArgument }}
  If not provided, will list all subscriptions in the server.

## `/subscription info`

Get information about a subscription.

### Parameters

- `subscription` : {{ $var.subscriptionArgument }}

## `/subscription delete`

Delete a subscription.

### Parameters

- `subscription` : {{ $var.subscriptionArgument }}
