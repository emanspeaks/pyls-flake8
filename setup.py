from setuptools import find_packages, setup

desc = "Flake8 plugin for the Python Language Server"

setup(
      name="pyls-flake8",
      version="0.2.0",
      description=desc,
      long_description=desc,
      url="https://github.com/emanspeaks/pyls-flake8",
      author="Randy Eckman",
      author_email="emanspeaks@gmail.com",
      packages=find_packages(),
      install_requires=["python-language-server", "flake8>=3.6.0"],
      entry_points={"pyls": ["pyls_flake8 = pyls_flake8.plugin"]},
      classifiers=(
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3.7",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   ),
      )
