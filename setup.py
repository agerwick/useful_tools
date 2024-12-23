from setuptools import setup, find_packages
import subprocess

def get_last_commit_datetime():
    return subprocess.check_output(["git", "log", "-1", "--date=format:%Y.%m.%d.%H%M", "--format=%cd"]).strip().decode('utf-8')

setup(
    name='useful_tools',
    version=get_last_commit_datetime(),
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
    include_package_data=True, # the package data is included in the MANIFEST.in file
)