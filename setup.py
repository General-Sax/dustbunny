from distutils.core import setup

setup(
    name='dustbunny',
    version='0.1.0',
    packages=[
        'dustbunny',
        'dustbunny.adapters',
        'test',
    ],
    license='LICENSE.txt',
    long_description=open('README.md').read(),
)
