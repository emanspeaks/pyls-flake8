import os
from setuptools import find_packages, setup


def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


setup(
    name="pyls-flake8",
    version="0.4.0",
    description="A Flake8 plugin for the Python Language Server",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/emanspeaks/pyls-flake8",
    license="MIT",
    maintainer="Peter Justin",
    maintainer_email="peter.justin@outlook.com",
    author="Randy Eckman",
    author_email="emanspeaks@gmail.com",
    packages=find_packages(),
    install_requires=["python-lsp-server", "flake8>=3.6.0"],
    entry_points={"pylsp": ["pyls_flake8 = pyls_flake8.plugin"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
