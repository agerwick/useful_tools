from setuptools import setup, find_packages
from useful_tools import get_last_commit_datetime

setup(
    name='useful_tools',
    version=0, #get_last_commit_datetime(),
    packages=find_packages(),
    description='A collection of useful decorators and other tools I use on various projects',
    author='Ronny Ager-Wick',
    author_email='ronny@ager-wick.com',
    url='https://github.com/agerwick/useful_tools',
    install_requires=[
        'psutil'
    ],
    classifiers=[
        'Development Status :: 2 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
)