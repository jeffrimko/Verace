from setuptools import setup, find_packages

setup(
    name = "verace",
    version = "0.2.3",
    author = "Jeff Rimko",
    author_email = "jeffrimko@gmail.com",
    description = "Library for checking version strings in project files.",
    license = "MIT",
    url = "https://github.com/jeffrimko/Verace",
    py_modules=["verace"],
    long_description=open("README.rst").read(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Programming Language :: Python :: 2.7",
    ],
)
