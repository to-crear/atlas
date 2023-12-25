from setuptools import setup, find_packages


VERSION = "0.0.0"

setup(
   name="atlas",
   version=VERSION,
   packages=find_packages(),
   install_requires=[],
    author="To Crear",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    entry_points={"console_scripts": ["atlas = atlas.atlas:main"]},
    scripts=["bin/atlas.cmd"],
)
