from setuptools import setup, find_packages # type: ignore

setup(
    name="swf",
    version="1.0",
    author="NathaanTFM",
    description="Python SWF file reader.",
    packages=find_packages(include=["swf*"])
)

