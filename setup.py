from setuptools import setup, find_packages

setup(
    name='SignalBot',
    version='0.1.4',
    description='Interactive bot for the Signal messenger platform',
    packages=['signalbot'],
    author='Patrick Blaas',
    author_email='patrick@kite4fun.nl',
    license='MIT',
    install_requires=['pytest', 'pytest-html', 'pytest-cov', 'pytest-dotenv', 'docker', 'haikunator', 'emoji', 'urllib3']
)
