# Azure KeyVault Secrets as Environment Variable

Get Azure KeyVault variables ans use them as environment variables.

## Install 

```bash
pip install azsecrets
```

## Usage

You can set environment variables for:

```bash
export AZURE_VAULT_BASE_URL=***
export AZURE_CLIENT_ID=***
export AZURE_SECRET_KEY=***
export AZURE_TENANT_ID=***
```

or send it via the CLI as

```bash
secrets --vault-base-url *** --client-id *** --secret *** --tenant *** env --shell bash
```

Once you have set up the environment variables, just call the CLI:

```bash
secrets env --shell bash
```

You can also use it at as an package my importing it:

```python
from azsecrets import AzureSecrets

print(AzureSecrets().get_secret("SECRET-NAME"))
print(AzureSecrets().get_secrets(["SECRET-NAME-1", "SECRET-NAME-1"]))
```

## Contributions

All contributions are welcome.
