from distutils.core import setup # type: ignore
from setuptools import find_packages

setup(
    name="swf",
    version="1.0",
    author="NathaanTFM",
    description="Python SWF file reader.",
    packages=find_packages(include=["swf*"])
)

