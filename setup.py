#!/usr/bin/env python

# Copyright 2019-2020 CivicActions, Inc. See the README file at the top-level
# directory of this distribution and at https://github.com/CivicActions/compliancetools#copyright.

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
        "pypandoc",
        "openpyxl"
    ],
    entry_points = {
        "console_scripts": [
            "createfiles=createfiles.createfiles:main",
            "creatematrix=creatematrix.creatematrix:main",
            "exportto=exportto.exportto:main",
            "makefamilies=makefamilies.makefamilies:main",
            "makessp=makessp.makessp:main",
            "selectcontrols=selectcontrols.selectcontrols:main",
            "status=status.status:main",
            "xlwriter=xlwriter.xlwriter:main"
        ]
    }
)
