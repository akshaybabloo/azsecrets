import os

import click
import sys
from azure.common.credentials import ServicePrincipalCredentials
from azure.keyvault import KeyVaultClient, KeyVaultAuthentication

__version__ = '1.0'


class AzureSecrets:
    """
    Azure secrets object that can be used for CLI and as a module.
    """

    def __init__(self, vault_base_url: str = None, client_id: str = None, secret: str = None,
                 tenant: str = None,
                 env_names: list = None):

        self.vault_base_url = vault_base_url
        self.client_id = client_id
        self.secret = secret
        self.tenant = tenant
        self.env_names = env_names

        try:
            if self.vault_base_url is None:
                self.vault_base_url = os.environ["AZURE_VAULT_BASE_URL"]
            if self.client_id is None:
                self.client_id = os.environ['AZURE_CLIENT_ID']
            if self.secret is None:
                self.secret = os.environ['AZURE_SECRET_KEY']
            if self.tenant is None:
                self.tenant = os.environ['AZURE_TENANT_ID']
        except KeyError as e:
            print("Did you forget to set the environment variable?", e)
            sys.exit(1)

        self.client = KeyVaultClient(KeyVaultAuthentication(_auth_callback))

    def get_secret(self, secret_name: str, secret_version: str = None) -> str:
        """
        Get the value for the secret key.

        :param secret_name: Name of the secret key.
        :type secret_name: str
        :param secret_version: The version string of the secret key.
        :type secret_version: str
        :return: The secret value.
        :rtype: str

        >>> secrets = AzureSecrets('https://', 'client id', 'secret key', 'tenant id')
        >>> print(secrets.get_secret('secret-name'))
        secret-value
        """
        if secret_version is None:
            secret_version = os.environ.get("SECRET_VERSION", "")

        key_bundle = self.client.get_secret(self.vault_base_url, secret_name, secret_version)

        return key_bundle.value

    def get_secrets(self, env_names: list = None) -> dict:
        """
        A dictionary of secret name and it's value.

        :param env_names: A list of secret names.
        :type env_names: list
        :rtype: dict
        :return: Dictionary of secrets.

        >>> secrets = AzureSecrets('https://', 'client id', 'secret key', 'tenant id')
        >>> print(secrets.get_secret(['secret-name-1', 'secret-name-2']))
        {
            'secret-name-1' : 'secret-value-1',
            'secret-name-2': 'secret-value-2'
        }
        """
        secrets = {}

        key_bundle = self.client.get_secrets(self.vault_base_url)

        if self.env_names is None or env_names is None:
            for secret_id in key_bundle:
                _secret_id = secret_id.as_dict()['id'].split('/').pop()
                secrets.update({_secret_id: self.get_secret(secret_name=_secret_id)})
        else:
            for secret_name in self.env_names:
                secrets.update({secret_name: self.get_secret(secret_name=secret_name)})

        return secrets

    def env_powershell(self):
        """
        Prints environment variable for PowerShell
        """
        for key, value in self.get_secrets().items():
            print(f"$Env:{key}={value}")
        print("# Run this command to configure your shell:")
        print("# & python azure_env.py env --shell powershell | Invoke-Expression")

    def env_cmd(self):
        """
        Prints environment variable for CMD
        """
        for key, value in self.get_secrets().items():
            print(f"SET {key}={value}")
        print("REM Run this command to configure your shell:")
        print("REM @FOR /f \"tokens=*\" %i IN ('python azure_env.py env --shell cmd') DO @%i")

    def env_bash(self):
        """
        Prints environment variable for Bash
        """
        for key, value in self.get_secrets().items():
            print(f"export {key}={value}")
        print("# Run this command to configure your shell:")
        print("# eval $(python azure_env.py env --shell bash)")


def _auth_callback(server, resource, scope):
    credentials = ServicePrincipalCredentials(
        client_id=os.environ['AZURE_CLIENT'],
        secret=os.environ['AZURE_KEY'],
        tenant=os.environ['AZURE_TENANT_ID'],
        resource=resource
    )

    token = credentials.token
    return token['token_type'], token['access_token']


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()


@click.group()
@click.option('--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True,
              help="Show version and exit.")
@click.option('--vault-base-url', help='Azure KeyVault base URL. Defaults to None.', default=None)
@click.option('--client-id', help='Azure KeyVault client ID.', default=None)
@click.option('--secret', help='Azure KeyVault secret.', default=None)
@click.option('--tenant', help='Azure tenant ID.', default=None)
@click.pass_context
def cli(ctx, vault_base_url, client_id, secret, tenant):
    ctx.obj['vault_base_url'] = vault_base_url
    ctx.obj['client_id'] = client_id
    ctx.obj['secret'] = secret
    ctx.obj['tenant'] = tenant


@cli.command(help="Environment configuration: [powershell, cmd or bash].")
@click.option('--shell', type=click.Choice(['powershell', 'cmd', 'bash']))
@click.pass_context
def env(ctx, shell):
    if shell == 'powershell':
        AzureSecrets(ctx.obj['vault_base_url'], ctx.obj['client_id'], ctx.obj['secret'],
                     ctx.obj['tenant']).env_powershell()
    elif shell == 'cmd':
        AzureSecrets(ctx.obj['vault_base_url'], ctx.obj['client_id'], ctx.obj['secret'],
                     ctx.obj['tenant']).env_cmd()
    elif shell == 'bash':
        AzureSecrets(ctx.obj['vault_base_url'], ctx.obj['client_id'], ctx.obj['secret'],
                     ctx.obj['tenant']).env_bash()


def main():
    cli(obj={})


if __name__ == '__main__':
    cli(obj={})