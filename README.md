# vendored-conda-builds

This is a repository to create Conda builds of 3rd party packages and upload them to the
[labscript-suite Anaconda Cloud repository](https://anaconda.org/labscript-suite/repo).

This way these packages (which are otherwise not available in the conda repository) can
be made available to labscript-suite users using conda. We also may make packages
available on the labscript-suite Anaconda Cloud repository even if they are available on
conda-forge, to reduce the need for users to use conda-forge to obtain packages not in
the main conda repository.

Please file an issue if you notice a package is out of date or any other issues with the
conda packages produced by this repository.

A list of packages currently built in this repository can be found in `pkgs.toml`. The
script `make_packages.py` executes the build, and it in turn is run by a github action
in `.github/workflows/make_packages.yml` whenever a new commit is pushed to this
repository. If the packages build sucessfully, the github action uploads them to the
labscript-suite Anaconda Cloud repository.
