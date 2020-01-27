#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages

setup(
    name="compliancetools",
    description="Tools for generating compliance documents.",
    version="0.1",
    author="Tom Camp",
    author_email="tom.camp@civicactions.com",
    license="CC",
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        "click",
        "md-toc",
        "pyyaml",
        "pyyaml-include",
        "rtyaml",
    ],
    entry_points = {
        "console_scripts": [
            "createfiles=createfiles.createfiles:main",
            "makefamilies=makefamilies.makefamilies:main",
            "makessp=makessp.makessp:main",
        ]
    }
)