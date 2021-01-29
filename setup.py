from setuptools import setup, find_packages

setup(
    name='SignalBot',
    version='0.1.3',
    description='Interactive bot for the Signal messanger platform',
    packages=['signalbot'],
    author='Patrick Blaas',
    author_email='patrick@kite4fun.nl',
    license='MIT',
    install_requires=['pytest', 'docker', 'haikunator', 'emoji', 'urllib3']
)
