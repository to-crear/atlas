from setuptools import find_packages, setup

VERSION = "0.0.0"
requirements = [line.strip() for line in open("requirements.txt").readlines()]

setup(
    name="atlas",
    version=VERSION,
    packages=find_packages(),
    install_requires=requirements,
    author="To Crear",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    entry_points={"console_scripts": ["atlas = atlas.atlas:main"]},
    scripts=["bin/atlas.cmd"],
)
