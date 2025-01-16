"""Setup configurations"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme_file:
    description = readme_file.read()

setup(
    name="unofficial_tabdeal_api",
    version="0.0.1",
    packages=find_packages(),
    requires=["aiohttp>=3.11.11"],
    long_description=description,
    long_description_content_type="text/markdown",
)
