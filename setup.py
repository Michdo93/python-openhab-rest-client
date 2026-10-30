from setuptools import setup, find_packages

setup(
    name="python-openhab-rest-client",
    version="21.4.0",
    packages=find_packages(exclude=["tests", "tests.*", "tests_pytest", "tests_pytest.*", "tools"]),
    install_requires=[
        "requests>=2.28",
        "aiohttp>=3.9",
    ],
    author="Michael Christian Dörflinger",
    author_email="michaeldoerflinger93@gmail.com",
    description="A Python client for the openHAB REST API. This library enables easy interaction with the openHAB REST API to control smart home devices, retrieve status information, and process events.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Michdo93/python-openhab-rest-client",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Home Automation",
    ],
    python_requires=">=3.8",
)
