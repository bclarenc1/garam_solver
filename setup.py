"""Setup"""

from setuptools import find_packages, setup

with open("requirements.txt", "r", encoding="utf-8") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='solver',
      version="0.0.1",
      install_requires=requirements,
      packages=find_packages())
