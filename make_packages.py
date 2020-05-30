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

if platform.system() == 'Windows' and sys.maxsize > 2 ** 32:
    PLATFORM = 'win-62'
elif platform.system() == 'Windows':
    PLATFORM = 'win-32'
elif platform.system() == 'Linux':
    PLATFORM = 'linux'
elif platform.system() == 'Dawrin':
    PLATFORM = 'osx'
else:
    raise ValueError(platform.system())


def build_conda_package(name, spec):
    version = spec.get('version', defaults['version'])
    pythons = spec.get('pythons', defaults['pythons'])
    platforms = spec.get('platforms', defaults['platforms'])
    noarch = spec.get('noarch', defaults['noarch'])
    build_args = spec.get('build_args', defaults['build_args'])[:]

    if noarch and not os.getenv('BUILD_NOARCH'):
        return
    elif not noarch:
        if PLATFORM not in platforms:
            return

        if f'{sys.version_info.major}.{sys.version_info.minor}' not in pythons:
            return

    name_with_version = name
    if version != 'latest':
        name_with_version += f'=={version}'

    # Download the sdist
    download_cmd = [
        'pip',
        'download',
        '--no-binary=:all:',
        '--no-deps',
        '--dest',
        'build',
        name_with_version,
    ]

    check_call(download_cmd)

    # Find the sdist
    for path in Path('build').iterdir():
        if path.stem.rsplit('-', 1)[0] == name and path.name.endswith('.tar.gz'):
            sdist = path
            break
    else:
        raise RuntimeError("Can't find sdist")

    # Unpack it
    check_call(['tar', 'xvf', sdist, '-C', 'build'])

    project_dir = Path('build', sdist.name.rsplit('.tar.gz', 1)[0])

    # Build it
    if noarch:
        build_args += ['--noarch']

    check_call(['setuptools-conda', 'build', *build_args, project_dir])

    for arch in Path(project_dir, 'conda_packages').iterdir():
        for package in arch.iterdir():
            dest = Path('conda_packages', arch.name, package.name)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(package, dest)


if __name__ == '__main__':
    Path('build').mkdir(exist_ok=True)
    packages = toml.load('pkgs.toml')
    defaults = packages['defaults']

    for name, spec in packages.items():
        if name == 'defaults':
            continue

        build_conda_package(name, spec)
