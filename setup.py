from setuptools import find_packages, setup

VERSION = "0.0.2"
requirements = [
    "click==8.1.7",
    "cloudpickle==3.0.0",
    "packaging==24.0",
    "pyyaml==6.0.1",
    "wheel==0.42.0",
]

setup(
    name="ml-atlas",
    version=VERSION,
    description="MLOps tool for building and maintaining machine learning models",
    url="https://github.com/tocrear/atlas",
    packages=find_packages(),
    install_requires=requirements,
    author="To Crear",
    author_email="tocrear.3@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["atlas = atlas.atlas:main"]},
    scripts=["bin/atlas.cmd"],
)
