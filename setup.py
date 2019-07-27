from setuptools import setup, find_packages
from setup_helper import install_from_git, prepare_setup, InstallCommand, install_by_pip

# This is the very first thing that needs to be called.
prepare_setup()

PACKAGE_VERSION = '3.4.3'

INTERNAL_DEPENDENCIES = [

]

INSTALL_REQUIRES = [
    'Django>=2.0.3,<3.0.0',
    'freezegun>=0.3.11,<1.0.0',
    'aiohttp==3.5.4',
    'python-dotenv==0.8.2'
]

setup(
    name='facebook_sdk',
    version=PACKAGE_VERSION,
    packages=find_packages(),
    include_package_data=True,
    description='Facebook messenger bot SDK for nj project',
    cmdclass={'install': InstallCommand}
)

[install_by_pip(dependency) for dependency in INSTALL_REQUIRES]
[install_from_git(*dependency) for dependency in INTERNAL_DEPENDENCIES]
