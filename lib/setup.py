from setuptools import setup, find_packages

setup(
    name = "verace",
    version = "0.1.0",
    author = "Jeff Rimko",
    author_email = "jeffrimko@gmail.com",
    description = "Library for creating version string checking scripts.",
    license = "MIT",
    url = "https://github.com/jeffrimko/Verace",
    py_modules=["verace"],
    long_description=__doc__,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Programming Language :: Python :: 2.7",
    ],
)
