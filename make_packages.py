import sys
import os
import toml
import platform
from subprocess import check_call
from pathlib import Path
import shutil


# This script is designed to run from GitHub actions, Github actions will run jobs for
# all of the platforms and Python versions we want to build packages for, and run this
# script in each of them. Our job is to build a conda package if the current platform
# and Python version is requested for a pacakge. Or, if it is a noarch package we only
# want to build it on one of the jobs, and it doesn't matter which one. So the GitHub
# workflow will set the environment variable BUILD_NOARCH=true for one of the jobs and
# there we will build noarch packages.

# This script must be run from within a conda environment with pip and setuptools-conda
# installed.

# Have had massive headaches with the filepaths being too long on GitHub Actions,
# causing conda-build to choke inexplicably. Allow a directory to be passed in as a
# command line arg. The workflow will pass in the value of runner.temp, which is a short
# filepath for a temporary directory we can use.
if len(sys.argv) > 1:
    BUILD_DIR = sys.argv[1]
else:
    BUILD_DIR = 'build'


if platform.system() == 'Windows' and sys.maxsize > 2 ** 32:
    PLATFORM = 'win-64'
elif platform.system() == 'Windows':
    PLATFORM = 'win-32'
elif platform.system() == 'Linux':
    PLATFORM = 'linux'
elif platform.system() == 'Dawrin':
    PLATFORM = 'osx'
else:
    raise ValueError(platform.system())


def download(name, source, version):
    """Download an  uncompress an sdist from given source and return the resulting
    directory"""
    # Download the sdist
    if source == 'pypi':
        name_with_version = name
        if version != 'latest':
            name_with_version += f'=={version}'

        download_cmd = [
            'pip',
            'download',
            '--no-binary=:all:',
            '--no-deps',
            '--dest',
            BUILD_DIR,
            name_with_version,
        ]
    else:
        download_cmd = ['pip', 'download', '--dest', BUILD_DIR, source]

    check_call(download_cmd)

    # Find it:
    for path in Path(BUILD_DIR).iterdir():
        if path.stem.rsplit('-', 1)[0] == name:
            if path.name.endswith('.zip'):
                extension = '.zip'
                break
            if path.name.endswith('.tar.gz'):
                extension = '.tar.gz'
                break
    else:
        raise RuntimeError("Can't find sdist")

    # Decompress it:
    base = Path(BUILD_DIR, path.name.rsplit(extension, 1)[0])
    if extension == '.tar.gz':
        check_call(['tar', 'xvf', str(path), '-C', BUILD_DIR])
    elif extension == '.zip':
        check_call(['unzip', str(path), '-d', BUILD_DIR])
    if source.startswith('git+'):
        return Path(BUILD_DIR, source.strip('/').split('/')[-1])
    else:
        return base


def build_conda_package(name, spec):
    version = spec.get('version', defaults['version'])
    source = spec.get('source', defaults['source'])
    noarch = spec.get('noarch', defaults['noarch'])
    build_args = spec.get('build_args', defaults['build_args'])[:]
    pythons = spec.get('pythons', defaults['pythons'])
    platforms = spec.get('platforms', defaults['platforms'])

    if noarch and not os.getenv('BUILD_NOARCH'):
        print(f"Skipping {name} as it is noarch but BUILD_NOARCH env var is not set")
        return
    elif not noarch:
        if PLATFORM not in platforms:
            print(f"Skipping {name} as {PLATFORM} is not in its list of platforms")
            return

        PY = f'{sys.version_info.major}.{sys.version_info.minor}'
        if PY not in pythons:
            print(f"Skipping {name} as {PY} is not in its list of Python versions")
            return

    # Download it:
    project_dir = download(name, source, version)

    # Build it
    if noarch:
        build_args += ['--noarch']

    check_call(['setuptools-conda', 'build', *build_args, str(project_dir)])

    for arch in Path(project_dir, 'conda_packages').iterdir():
        for package in arch.iterdir():
            dest = Path('conda_packages', arch.name, package.name)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(package, dest)


if __name__ == '__main__':
    Path(BUILD_DIR).mkdir(exist_ok=True)
    packages = toml.load('pkgs.toml')
    defaults = packages['defaults']

    for name, spec in packages.items():
        if name == 'defaults':
            continue

        build_conda_package(name, spec)
