
from distutils.core import setup

with open('README.txt') as file:
    long_description = file.read()

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Topic :: Scientific/Engineering :: Visualization"
]

setup(
    name = "python-ternary",
    version = "1.0.1",
    packages=['ternary'],

    install_requires = ["matplotlib>=1.4"],

    author = "Marc Harper",
    author_email = "marc.harper@gmail.com",
    classifiers = classifiers,
    description = "Make ternary plots in matplotlib",
    long_description=long_description,
    keywords = "matplotlib ternary plotting",
    license = "MIT",

    url = "https://github.com/marcharper/python-ternary",
    download_url = "https://github.com/marcharper/python-ternary/tarball/1.0.1",
)
