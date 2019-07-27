from __future__ import print_function

import re
import subprocess
import sys

from setuptools.command.install import install

ENVIRONMENT = None


class InstallCommand(install):
    user_options = install.user_options + [
        ('environment=', None, 'Specify a production or development environment.'),
    ]

    def initialize_options(self):
        install.initialize_options(self)
        self.environment = None

    def finalize_options(self):
        install.finalize_options(self)

        global ENVIRONMENT

        try:
            # Check if environment is set
            is_dev()
        except AssertionError:
            # If not - assert that this class has a set environment
            assert self.environment in ['dev', 'prod'], 'Bad environment propagated from parent project.'
            ENVIRONMENT = self.environment

    def run(self):
        install.run(self)


def resolve_version(version_to_resolve, git_repository, dev=True):
    """
    Resolves a git tagged version. E.g. If version to resolve is 2.*.*, function fetches all
    tags from a provided git repository and assigns latest tags to wildcards in version to resolve string.

    :return: Resolved version string or None if resolve failed.
    """
    # Split version to resolve string into major, minor and patch versions
    major, minor, patch = version_to_resolve.split('.')

    # Regex to match only those versions that contain only numbers, digits and a string 'dev-'
    regex = re.compile(r'^[dev\-0-9.]*$')

    # Fetch all tags from a git repository
    output = subprocess.check_output(
        ['git', 'ls-remote', '--tags', 'ssh://git@bitbucket.org/{}.git'.format(git_repository)])
    # Split and filter out standard git api output and leave only tag strings
    output = [line.split('\t')[1].split('/')[2] for line in output.decode().splitlines()]
    # Filter our tags that do not match version structure (e.g. dev-2.0.0 or 1.5.0)
    output = list(filter(regex.search, output))

    # Separate development versions
    dev_versions = [version.replace('dev-', '') for version in output if version.__contains__('dev')]
    # Separate production versions
    prod_versions = [version for version in output if not version.__contains__('dev')]

    # Set versions list to work with depending on environment (dev or prod)
    versions = dev_versions if dev else prod_versions

    # Split version strings  into a list of 3 integers: major, minor and patch versions
    versions = [[int(version) for version in version_string.split('.')] for version_string in versions]
    # Sort in reverse versions so the latest version would be at index 0
    versions.sort(key=lambda version: (version[0], version[1], version[2]), reverse=True)

    # Create a function that resolves each subversion independently
    def resolve_subversion(versions, index, subversion):
        if subversion != '*':
            versions = [vrs for vrs in versions if vrs[index] == int(subversion)]
        return versions, versions[0][index]

    try:
        # Resolve major version first
        versions, resolved_major = resolve_subversion(versions, 0, major)
        # Resolve minor version second
        versions, resolved_minor = resolve_subversion(versions, 1, minor)
        # Resolve patch version last
        versions, resolved_patch = resolve_subversion(versions, 2, patch)
    except IndexError:
        print('Failed to resolve version for: {}'.format(version_to_resolve))
        return None

    # Return a resolved version string which corresponds to input version to resolve
    return str(resolved_major) + '.' + str(resolved_minor) + '.' + str(resolved_patch)


def install_from_git(name, version, url_path):
    """
    Installs a python package from a git repository.
    """
    if not is_installing():
        return

    # Resolve supplied version with git tags
    dependency_version = resolve_version(version, url_path, is_dev())
    # Make sure version was resolved
    assert dependency_version, 'Bad version supplied for {}. Version: {}'.format(name, version)
    print("Resolved version for {}: {}".format(version, dependency_version))
    # Create a dependency link
    dep_link = 'git+ssh://git@bitbucket.org/{}.git@{}'.format(url_path, ("dev-" if is_dev() else '') + dependency_version)

    # Install dependency through pip
    command = [sys.executable, "-m", "pip", "install", dep_link]
    command.extend(['--install-option=--environment={}'.format('dev' if is_dev() else 'prod')])
    subprocess.check_call(command)


def install_by_pip(dependency):
    if not is_installing():
        return

    # Install dependency through pip
    command = [sys.executable, "-m", "pip", "install", dependency]
    subprocess.check_call(command)


def is_installing():
    return "install" in sys.argv


def is_dev():
    """
    Determines whether setup is running in development or production environment
    """
    dev = "dev" == ENVIRONMENT
    prod = "prod" == ENVIRONMENT

    assert (prod or dev) is True, 'Environment should be set to dev or prod'
    assert (prod and dev) is False, 'Environment can not be both prod and dev at the same time'

    return dev


def prepare_setup():
    """
    Ensures that setup() can be called without errors and environment is set.
    """
    if not is_installing():
        return

    global ENVIRONMENT

    if "dev" in sys.argv:
        sys.argv.remove("dev")
        ENVIRONMENT = "dev"

    if "prod" in sys.argv:
        sys.argv.remove("prod")
        ENVIRONMENT = "prod"
