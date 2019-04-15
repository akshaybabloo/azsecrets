As a Command Line Interface
===========================

If you are using a docker and you want to set your environment variables, this package can help you do so. The idea is borrowed from ``docker-machine env``.

It supports three shell types:

1. PowerShell - ``secrets env --shell powershell``
2. CMD - ``secrets env --shell cmd``
3. Bash - ``secrets env --shell bash``

.. warning::

    PowerShell does not take ``-`` as environment names, and Azure Key Vault does not consider ``-`` as a correct character. When using PowerShell
    ``-`` is converted to ``_``.

    .. versionadded:: 1.0.2

Setting up Shell before using Secrets
-------------------------------------

There are two ways to give in the Azure KeyVault credentials, either set environment variables for:

.. code-block:: bash
    :caption: For bash terminal

    export AZURE_VAULT_BASE_URL=***
    export AZURE_CLIENT_ID=***
    export AZURE_SECRET_KEY=***
    export AZURE_TENANT_ID=***

or provide them via the CLI arguments

.. code-block:: bash

    secrets --vault-base-url *** --client-id *** --secret *** --tenant *** env --shell bash

Comma Separated Names
---------------------

You can now use comma separated names as input, instead of getting all the keys. To do this type in:

.. code-block:: bash

    secrets env --shell bash --secret-names SECRET-1,SECRET-2

.. versionadded:: 1.0.1

Arguments and Commands
----------------------

For more information, type in ``secrets --help`` or ``secrets env --help``.

.. code-block::
    :caption: secrets --help

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
      env                    Environment configuration: [powershell, cmd or bash].

.. code-block::
    :caption: secrets env --help

    Usage: secrets env [OPTIONS]

    Environment configuration: [powershell, cmd or bash].

    Options:
      --shell [powershell|cmd|bash]
      --secret-names TEXT            A comma separated names of the secret to use
                                     (without space): NAME-1,NAME-2
      --help                         Show this message and exit.