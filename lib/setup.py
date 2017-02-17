from os.path import isfile
from setuptools import setup, find_packages

setup(
    name = "verace",
    version = "0.3.0-alpha2",
    author = "Jeff Rimko",
    author_email = "jeffrimko@gmail.com",
    description = "Library for checking version strings in project files.",
    license = "MIT",
    keywords = "project files version check library",
    url = "https://github.com/jeffrimko/Verace",
    py_modules=["verace"],
    long_description=open("README.rst").read() if isfile("README.rst") else "",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Programming Language :: Python :: 2.7",
    ],
)
