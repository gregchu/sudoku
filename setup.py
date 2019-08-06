from setuptools import setup

reqs = None
with open("requirements.txt") as rf:
    reqs = rf.readlines()

setup(name="sudoku",
      python_requires='>3.6',
      install_requires=reqs,
)