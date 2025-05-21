from setuptools import setup, find_packages

setup(
    name="challenge_project",
    version="0.1",
    packages=find_packages(include=["scripts", "scripts.*", "config", "config.*"]),
    install_requires=[]
)