# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from setuptools import setup
from codecs import open  # To use a consistent encoding
from os import path

HERE = path.abspath(path.dirname(__file__))

# Get version info
ABOUT = {}
with open(path.join(HERE, "datadog_checks", "prometheus", "__about__.py")) as f:
    exec(f.read(), ABOUT)

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Parse requirements
def get_requirements(fpath):
    with open(path.join(HERE, fpath), encoding='utf-8') as f:
        return f.readlines()


setup(
    name='datadog-prometheus',
    version=ABOUT["__version__"],
    description='The prometheus check',
    long_description=long_description,
    keywords='datadog agent prometheus check',

    # The project's main homepage.
    url='https://github.com/DataDog/integrations-core',

    # Author details
    author='Datadog',
    author_email='packages@datadoghq.com',

    # License
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Monitoring',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    # The package we're going to ship
    packages=['datadog_checks.prometheus'],

    # Run-time dependencies
    install_requires=[
        'datadog-checks-base',
    ],

    # Development dependencies, run with:
    # $ pip install -e .[dev]
    extras_require={
        'dev': [
            'check-manifest',
        ],
    },

    # Testing setup and dependencies
    setup_requires=['pytest-runner',],
    tests_require=get_requirements(path.join('tests', 'requirements.txt')),

    # Extra files to ship with the wheel package
    package_data={'datadog_checks.prometheus': ['conf.yaml.default']},
    include_package_data=True,
)
