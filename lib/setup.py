import os
import subprocess
from setuptools import setup, find_packages

subprocess.call("asciidoc -b docbook ../README.adoc", shell=True)
subprocess.call("pandoc -r docbook -w rst -o ../README.rst ../README.xml", shell=True)
os.remove("../README.xml")

setup(
    name = "verace",
    version = "0.2.0",
    author = "Jeff Rimko",
    author_email = "jeffrimko@gmail.com",
    description = "Library for checking version strings in project files.",
    license = "MIT",
    url = "https://github.com/jeffrimko/Verace",
    py_modules=["verace"],
    long_description=open("../README.rst").read(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Programming Language :: Python :: 2.7",
    ],
)

os.remove("../README.rst")
