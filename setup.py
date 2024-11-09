import setuptools
from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

with open("requirements.txt") as requirements_file:
    requirements = requirements_file.read().splitlines()

with open("ztf_api/_version.py") as version_file:
    for line in version_file:
        if "__version__" in line:
            __version__ = line.split()[-1].replace('"', "")

setuptools.setup(
    name="ZTF_api",
    version=2.0,
    author="Joan Alcaide-Núñez",
    author_email="joanalnu@outlook.com",
    license="MIT",
    description="API to access ZTF data from command lines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/joanalnu/ZTF_api',
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={"ztf_api": ["static/*"]},
    include_package_data=True,
)