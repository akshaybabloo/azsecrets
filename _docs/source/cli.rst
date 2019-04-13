As a Command Line Interface
===========================

If you are using a docker and you want to set your environment variables, this package can help you do so. The idea is borrowed from ``docker-machine env``.

It supports three shell types:

1. PowerShell - ``secrets env --shell powershell``
2. CMD - ``secrets env --shell cmd``
3. Bash - ``secrets env --shell bash``


Setting up Shell before using Secrets
-------------------------------------

There are two ways to give in the Azure KeyVault credentials, either set environment variables for:

.. code-block::

    AZURE_VAULT_BASE_URL=***
    AZURE_CLIENT_ID=***
    AZURE_SECRET_KEY=***
    AZURE_TENANT_ID=***

or provide them via the CLI arguments

.. code-block::

    > secrets --help

    Usage: secrets [OPTIONS] COMMAND [ARGS]...

    Options:
      --version              Show version and exit.
      --vault-base-url TEXT  Azure KeyVault base URL. Defaults to None.
      --client-id TEXT       Azure KeyVault client ID.
      --secret TEXT          Azure KeyVault secret.
      --tenant TEXT          Azure tenant ID.
      --help                 Show this message and exit.

    Commands:
      env                   Environment configuration: [powershell, cmd or bash].