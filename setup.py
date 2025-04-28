import re
import os
import setuptools

ver = '1.0.3'

with open("README.md", "r", encoding="utf-8") as fh:
    long_desc = fh.read()

desc = "DkBotzDB Is The Most Powerful And Developer-Friendly Database Solution Powered By DKBotz And DkBotzPro, Offering Fast, Reliable, Scalable, And Secure Data Management. Designed For Effortless Integration And Built With Modern API Standards, DkBotzDB Ensures Smooth Performance Across Applications, Backed By The Trust And Excellence of dkbotzpro.in."
GPL = "GNU AFFERO GENERAL PUBLIC LICENSE (v3)"
git = "https://github.com/DKBOTZPROJECT/DKBOTZDB"
classify = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
]
requirements = [
    "requests",
    "colorlog",
]


setuptools.setup(
    name="dkbotzdb",
    version=ver,
    author="DKBOTZ",
    description=desc,
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url=git,
    license=GPL,
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=classify,
    python_requires=">=3.6",
)
