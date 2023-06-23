from setuptools import setup

setup(
    name="hn",
    version="0.1.0",
    py_modules=["hn"],
    install_requires=[
        "Click",
        "Httpx",
        "NLTK",

    ],
    entry_points={
        "console_scripts": [
            "hn = hn.cli:commands",
        ],
    },
)
