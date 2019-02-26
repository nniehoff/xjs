#!/usr/bin/env python3
# REFRENCE https://packaging.python.org/
import setuptools

requirements = [
    'PyYAML==3.13',
    'prettytable==0.7.2',
    'click==7.0',
    'packaging==19.0',
    'requests==2.21.0',
    'pendulum==2.0.4'
]

setuptools.setup(
    name="xjs",
    version="0.1",
    scripts=[
        "xjs",
    ],
)
