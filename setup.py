import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fmi-weather-client",
    version="0.5.0",
    author="Mika Hiltunen",
    author_email="saaste@gmail.com",
    description="Library for fetching weather information from Finnish Meteorological Institute (FMI)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saaste/fmi-weather-client",
    packages=setuptools.find_packages(exclude=["*test", "*test.*"]),
    install_requires=[
        'requests>=2.32.3',
        'xmltodict>=0.13.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9.20',
)
