from setuptools import setup, find_packages

setup(
    name="blackbox",
    description="A tool to test different inputs for any given program.",
    version="0.0.0",
    author="Chris Webster",
    maintainer="Chris Webster",
    url="",
    packages=find_packages(),
    entry_points={
        'console_scripts' : [
            'blackbox = blackbox.main:main'
        ]
    }
)