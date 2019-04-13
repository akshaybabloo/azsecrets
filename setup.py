import codecs
import os

from setuptools import setup

from azsecrets import __version__

here = os.path.abspath(os.path.dirname(__file__)) + os.sep


def get_requirements(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read().splitlines()


setup(
    name='azsecrets',
    version=__version__,
    install_requires=get_requirements('requirements.txt'),
    packages=['azsecrets'],
    url='https://github.com/akshaybabloo/azure-keyvault-secret-env',
    license='MIT',
    author='Akshay Raj Gollahalli',
    author_email='akshay@gollahalli.com',
    description='Set Azure Secrets as environment variables.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'secrets = azsecrets:main'
        ]
    }
)
