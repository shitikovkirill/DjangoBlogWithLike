#!/usr/bin/env python
import setuptools

with open("README.md") as fp:
    long_description = fp.read()

setuptools.setup(
    name="StarNaviTest",
    version="1.0",
    description="Test task",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "django==2.2.22",
        "djangorestframework==3.10.3",
        "drf-jwt==1.13.2",
        "drf-access-policy==0.4.2",
    ],
    python_requires=">=3.6",
    scripts=["manage.py"],
)
