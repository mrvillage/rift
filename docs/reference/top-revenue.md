# `/top-revenue`

The top-revenue command group provides revenue information about
the top nations/alliances as specified.

## `/top-revenue alliances`

Shows the top revenues for all alliances. For performance, it
by default only checks the top twenty-five alliances.

### Parameters

- `top_fifty` : Calculate revenue of the top fifty alliances
  instead of the top twenty five.

## `/top-revenue nations`

Shows the top revenue for all nations. For performance, it only
checks the top fifty nations.

## `/top-revenue alliance`

Shows the top revenue information of all nations in an alliance.

### Parameters

- `alliance` : {{ $var.allianceArgument }}
