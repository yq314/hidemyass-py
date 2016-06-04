# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name="hidemyass",
    author="Qing YE",
    author_email="2chin.yip@gmail.com",
    entry_points={
        "console_scripts": [
            "hidemyass = hidemyass.cli:fetch"
        ]
    },
    install_requires=install_requires,
    version="1.0",
    packages=find_packages()
)
