"""
Setup script for Signal Soup
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="signal-soup",
    version="0.1.0",
    author="Andrea Valle",
    author_email="andrea.valle@unito.it",
    description="A computational model exploring emergent communication through semiotic sign functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vanderaalle/signal-soup",
    py_modules=["signalSoup"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "graphviz>=0.19",
    ],
    keywords="multi-agent semiotics communication emergence language-evolution",
    project_urls={
        "Bug Reports": "https://github.com/vanderaalle/signal-soup/issues",
        "Source": "https://github.com/vanderaalle/signal-soup",
    },
)
