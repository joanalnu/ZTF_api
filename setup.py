import setuptools

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

with open("requirements.txt") as requirements_file:
    requirements = requirements_file.read().splitlines()

setuptools.setup(
    name="ZTF_api",
    version=1.0,
    author="Joan Alcaide-Núñez",
    author_email="joanalnu5@gmail.com",
    license="MIT",
    description="API to access ZTF data from command lines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joanalnu/ZTF_api",
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    package_data={"ztf_api": ["static/*"]},
    include_package_data=True,
)