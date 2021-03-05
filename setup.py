"""Add support for Sentry notifications.
"""

from os import path
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md')) as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="backwork-notifier-http",
    version="0.1.4",
    description="Backwork plug-in for HTTP notifications.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/IBM/backwork-notifier-http",
    author="Ben Honda",
    author_email="benhonda@ibm.com",
    license="Apache 2",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
        'License :: OSI Approved :: Apache Software License',
        "Topic :: Database",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: Utilities"
    ],
    packages=find_packages(),
    install_requires=[
        "backwork",
        "requests==2.25.1"
    ],
    entry_points={
        "backwork.notifiers": [
            "http=http_request:HTTPRequestNotifier"
        ]
    }
)
