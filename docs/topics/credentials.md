# Credentials

## What are credentials?

Credentials is the word for your Politics and War username,
password, and API key. Credentials allow Rift to interact with
the game as your account or another account, enabling things like
bank commands.

## How are credentials stored?

Credentials are stored in the database and users are only able to
view and edit their own credentials. Not only that, but
credentials are also RSA encrypted with a 4096 bit key and the
RSA v1.5 PKCS1 encryption scheme, meaning it's encrypted more heavily
than your internet traffic and can only be decrypted by a private key
held only by the bot itself.

## Why should I give my credentials?

By giving your credentials you allow Rift to use your account to perform
**the actions you allow it to with the permissions you allocate**. Meaning
that if you only give the `View Alliance Bank` permission, then Rift can't
do anything with your credentials except use them to view the balance
of your alliance bank, and only when a user with the proper permissions
given by your alliance does the action.

## How do I give my credentials?

You can give your credentials by heading to the credentials page on
the Rift dashboard
[here](https://rift.mrvilage.dev/dashboard/me/credentials). There you can fill
in the text boxes and the permissions you want to give.

## Permissions

::: danger Important note
**Only users with proper authentication are able to perform actions that
require credentials. Rift also picks the best credentials to do the job,
there is no way for the user to pick what credentials Rift uses for an action.
Rift will never use credentials to perform actions that are not allowed by
the permissions you give your credentials.**
:::

- `Send Nation Bank` : Allows you to send your nation's bank manually or through
  an automatic deposit.
- `Send Alliance Bank` : Allows Rift to use your credentials when sending your
  alliance bank.
- `View Nation Bank` : Allows you to view your nation's bank.
- `View Alliance Bank` : Allows Rift to use your credentials when
  displaying or calculating your alliance bank.
- `Manage Alliance Treaties` : Allows Rift to use your account when managing
  alliance treaties.
- `Manage Alliance Positions` : Allows Rift to use your account when managing
  in-game alliance positions.
- `Manage Alliance Taxes` : Allows Rift to use your account when managing
  alliance taxes.
- `Manage Alliance Announcements` : Allows Rift to use your account when
  managing
  alliance announcements.
- `Manage Nation` : Allows you to manage your nation through Rift.
  (i.e. Domestic Policy, War Policy, name, leader name, color, etc)
- `Send Messages` : Allows Rift to use your account when sending in-game messages.
- `Create Trade` : Allows you to create trades through Rift.
- `Manage Trades` : Allows you to accept, decline, or remove trades through Rift.
- `Declare War` : Allows you to declare war through Rift.
- `Manage Wars` : Allows you to manage your wars through Rift, primarily by
  doing attacks.
