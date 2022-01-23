# `/bank`

The bank command group provides a set of utilities for managing
bank related features.

## `/bank transfer`

Transfer money from an alliance bank.

### Parameters

- `recipient` : {{ $var.nationOrAllianceArgument}}
- `resources` : {{ $var.resourcesArgument }}
- `alliance` : The alliance to send money from. {{ $var.allianceArgument }}

## `/bank balance`

Show the balance of an alliance bank.

### Parameters

- `alliance` : {{ $var.allianceArgument }}

## `/bank account create`

Creates a new bank account for a user.

### Parameters

- `name` : The name of the bank account.
- `war_chest` : Whether the account balance counts towards war chest audits.
  {{ $var.defaultTrueArgument }}
- `alliance` : The alliance to create the bank account in.
  {{ $var.allianceArgument }}
- `primary` : Whether the account is your primary bank account.
  Defaults to false unless you don't have a primary account.

## `/bank account delete`

Deletes a bank account.

### Parameters

- `account` : {{ $var.bankAccountArgument }}

## `/bank account transfer`

Transfer resources from one bank account to another.

### Parameters

- `from` : {{ $var.bankAccountArgument }} {{ $var.primaryBankAccountDefaultArgument}}
- `to` : {{ $var.bankAccountArgument }}
- `amount` : {{ $var.resourcesArgument }}
- `note` : A note to attach to the transfer.

## `/bank account info`

Get information about a bank account.

### Parameters

- `account` : {{ $var.bankAccountArgument }}

## `/bank account list`

List a user's bank accounts in an alliance.

### Parameters

- `user` : {{ $var.memberOrUserArgument }}
- `alliance` : {{ $var.allianceArgument }}

## `/bank account edit`

Edit a bank account.

### Parameters

- `account` : {{ $var.bankAccountArgument }}
- `name` : The new name of the bank account.
- `war_chest` : Whether the account balance counts towards war chest audits.
  {{ $var.defaultTrueArgument }}
- `primary` : Whether the account is your primary bank account.
- `resources` : The new amount of resources in the account.

## `/bank account deposit`

Deposit resources into a bank account.

### Parameters

- `account` : {{ $var.bankAccountArgument }}
- `resources` : {{ $var.resourcesArgument }}
- `note` : A note to attach to the deposit.

## `/bank account deposit-check`

Check for new deposits to a bank account.

### Parameters

- `account` : {{ $var.bankAccountArgument }}

## `/bank account withdraw`

Withdraw resources from a bank account.

### Parameters

- `account` : {{ $var.bankAccountArgument }}
- `resources` : {{ $var.resourcesArgument }}
- `nation` : {{ $var.nationArgument }}
- `note` : A note to attach to the withdraw.

## `/bank account history`

View the transaction history of a bank account.

### Parameters

- `account` : {{ $var.bankAccountArgument }}
- `page` : The page of history to view.
- `status` : The status of the transactions to view. Can be `PENDING`,
  `ACCEPTED`, `REJECTED`, or `CANCELLED`. Defaults to all.

## `/bank transaction`

The bank transaction command group provides a set of utilities for
managing bank transactions.

## `/bank transaction review`

Review a pending bank transaction.

### Parameters

- `transaction` : {{ $var.transactionArgument }}
