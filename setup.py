import setuptools
from distutils.core import setup

version = "1.0.8"

with open('README.txt') as file:
    long_description = file.read()

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Topic :: Scientific/Engineering :: Visualization"
]

setup(
    name="python-ternary",
    version=version,
    packages=['ternary'],
    install_requires=["matplotlib>=2"],
    author="Marc Harper and contributors",
    author_email="marc.harper@gmail.com",
    classifiers=classifiers,
    description="Make ternary plots in python with matplotlib",
    long_description=long_description,
    keywords="matplotlib ternary plotting",
    license="MIT",
    url="https://github.com/marcharper/python-ternary",
    download_url="https://github.com/marcharper/python-ternary/tarball/{}".format(version),
)
