try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'USNASUAS Vision',
    'author': 'Connor Dittmar',
    'author_email': 'connor.dittmar@gmail.com',
    'version': '0.1';
    'install_requires': ['nose','interop'],
    'packages': ['vision'],
    'name': 'vision'
}

setup(**config)
