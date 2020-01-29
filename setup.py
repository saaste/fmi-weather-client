import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fmi_weather",
    version="0.0.1",
    author="Mika Hiltunen",
    author_email="saaste@gmail.com",
    description="Library for fetching weather information from Finnish Meteorological Institute (FMI)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saaste/fmi-weather",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6.9',
)
