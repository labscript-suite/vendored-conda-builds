<img src="https://raw.githubusercontent.com/labscript-suite/labscript-suite/master/art/labscript_32nx32n.svg" height="64" alt="the labscript suite" align="right">

# the _labscript suite_ » vendored-conda-builds

### Conda builds of vendored packages for the _labscript suite_

[![Actions Status](https://github.com/labscript-suite/vendored-conda-builds/workflows/Make%20and%20upload%20Conda%20packages/badge.svg)](https://github.com/labscript-suite/vendored-conda-builds/actions)
[![License](https://img.shields.io/github/license/labscript-suite/vendored-conda-builds)](https://github.com/labscript-suite/vendored-conda-builds/raw/master/LICENSE.txt)
[![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/labscript-suite/vendored-conda-builds)](https://github.com/labscript-suite/vendored-conda-builds/tags)


This repository is used to create Conda builds of the following packages and upload them to the
[labscript-suite Anaconda Cloud repository](https://anaconda.org/labscript-suite/repo).

| Package | Latest version | Conda version | Conda Platforms |
| :-- | :-- | :-- | :-- |
| [PyDAQmx](https://github.com/clade/PyDAQmx) | [![PyPI](https://img.shields.io/pypi/v/pydaqmx.svg)](https://pypi.org/project/pydaqmx) | [![Conda Version](https://img.shields.io/conda/v/labscript-suite/pydaqmx)](https://anaconda.org/labscript-suite/pydaqmx) | [![Conda Platforms](https://img.shields.io/conda/pn/labscript-suite/pydaqmx)](https://anaconda.org/labscript-suite/pydaqmx) |
| [pynivision](https://github.com/chrisjbillington/pynivision) | [![PyPI](https://img.shields.io/pypi/v/pynivision.svg)](https://pypi.org/project/pynivision) | [![Conda Version](https://img.shields.io/conda/v/labscript-suite/pynivision)](https://anaconda.org/labscript-suite/pynivision) | [![Conda Platforms](https://img.shields.io/conda/pn/labscript-suite/pynivision)](https://anaconda.org/labscript-suite/pynivision) |
| [pyqtgraph](https://github.com/pyqtgraph/pyqtgraph) | [![PyPI](https://img.shields.io/pypi/v/pyqtgraph.svg)](https://pypi.org/project/pyqtgraph) | [![Conda Version](https://img.shields.io/conda/v/labscript-suite/pyqtgraph)](https://anaconda.org/labscript-suite/pyqtgraph) | [![Conda Platforms](https://img.shields.io/conda/pn/labscript-suite/pyqtgraph)](https://anaconda.org/labscript-suite/pyqtgraph) |
| [spinapi](https://github.com/chrisjbillington/spinapi/) | [![PyPI](https://img.shields.io/pypi/v/spinapi.svg)](https://pypi.org/project/spinapi) | [![Conda Version](https://img.shields.io/conda/v/labscript-suite/spinapi)](https://anaconda.org/labscript-suite/spinapi) | [![Conda Platforms](https://img.shields.io/conda/pn/labscript-suite/spinapi)](https://anaconda.org/labscript-suite/spinapi) |
| [windows-curses](https://github.com/zephyrproject-rtos/windows-curses) | [![PyPI](https://img.shields.io/pypi/v/windows-curses.svg)](https://pypi.org/project/windows-curses) | [![Conda Version](https://img.shields.io/conda/v/labscript-suite/windows-curses)](https://anaconda.org/labscript-suite/windows-curses) | [![Conda Platforms](https://img.shields.io/conda/pn/labscript-suite/windows-curses)](https://anaconda.org/labscript-suite/windows-curses) |

These packages are not in the [default Anaconda repository](https://docs.anaconda.com/anaconda/user-guide/tasks/using-repositories/), and are made available to _labscript suite_ users with a conda installation via our [Anaconda cloud repository](https://anaconda.org/labscript-suite/repo). To reduce the need for users to use the [conda-forge respository](https://anaconda.org/conda-forge/repo), we may also build and publish packages in our Anaconda respository even if they are available on conda-forge.

Please file an [issue](https://github.com/labscript-suite/vendored-conda-builds/issues) if you notice a package is out of date or any other issues with the conda packages produced by this repository.


## Methodology

Whenever a new commit is pushed to this repository, the GitHub Action [`.github/workflows/make_packages.yml`](.github/workflows/make_packages.yml) runs the script [`make_packages.py`](make_packages.py), which executes the build of packages listed in [`pkgs.toml`](pkgs.toml). If the packages build sucessfully and the commit is tagged, the GitHub Action uploads them to the labscript-suite Anaconda Cloud repository. Additionally, the build and upload action is automatically run once per week on the latest tagged commit.
