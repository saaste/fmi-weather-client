import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fmi-weather-client",
    version="0.0.2",
    author="Mika Hiltunen",
    author_email="saaste@gmail.com",
    description="Library for fetching weather information from Finnish Meteorological Institute (FMI)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saaste/fmi-weather-client",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests>=2.22.0',
        'xmltodict>=0.12.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6.9',
)
