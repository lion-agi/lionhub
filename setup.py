import setuptools
import os

here = os.path.abspath(os.path.dirname(__file__))

# Get the code version
version = {}
with open(os.path.join(here, "lionhub/version.py")) as fp:
    exec(fp.read(), version)
__version__ = version["__version__"]

install_requires = [
    "lionagi", 
    "pandas", 
    "requests",
    "beautifulsoup4", 
    "yfinance", 
    "llama-index",
    "pyautogen"
]


setuptools.setup(
    name="lionhub",
    version=__version__,
    author="HaiyangLi",
    author_email="ocean@lionagi.ai",
    description="AGI tools, agents and solutions",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(include=["lionhub*"]),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
