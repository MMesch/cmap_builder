#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup script for SHTOOLS."""

from __future__ import absolute_import as _absolute_import
from __future__ import division as _division
from __future__ import print_function as _print_function

import os
import re
# the setuptools import dummy patches the distutil commands such that
# python setup.py develop works
import setuptools  # NOQA

from numpy.distutils.core import setup
from subprocess import CalledProcessError, check_output


# convert markdown README.md to restructured text .rst for pypi
# pandoc can be installed with
# conda install -c conda-forge pandoc pypandoc
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    print('no pandoc installed. Careful, pypi description will not be '
          'formatted correctly.')
    long_description = open('README.md').read()


# This flag has to be True if the version number indicated in the file
# VERSION has already been released and to False if this is a development
# version of a future release.
ISRELEASED = True


def get_version():
    """Get version from git and VERSION file.

    In case that the version is not tagged in git, this function appends
    .post0+commit if the version has been released and .dev0+commit if the
    version has not been released yet.

    Derived from: https://github.com/Changaco/version.py
    """
    d = os.path.dirname(__file__)
    # get release number from VERSION
    with open(os.path.join(d, 'VERSION')) as f:
        vre = re.compile('.Version: (.+)$', re.M)
        version = vre.search(f.read()).group(1)

    if os.path.isdir(os.path.join(d, '.git')):
        # Get the version using "git describe".
        cmd = 'git describe --tags'
        try:
            git_version = check_output(cmd.split()).decode().strip()[1:]
        except CalledProcessError:
            print('Unable to get version number from git tags\n'
                  'Setting to x.x')
            git_version = 'x.x'

        # PEP440 compatibility
        if '-' in git_version:
            # check that the version string is a floating number
            try:
                version = '{:.1f}'.format(float(version))
            except ValueError:
                msg = 'VERSION string should be floating number'
                raise ValueError(msg)
            git_revision = check_output(['git', 'rev-parse', 'HEAD'])
            git_revision = git_revision.strip().decode('ascii')
            # add post0 if the version is released
            # otherwise add dev0 if the version is not yet released
            if ISRELEASED:
                version += '.post0+' + git_revision[:7]
            else:
                version += '.dev0+' + git_revision[:7]

    return version


VERSION = get_version()
print('colormap2d package version: {}'.format(VERSION))


CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'  # NOQA
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Scientific/Engineering :: Physics'
]


KEYWORDS = ['2D Colormaps', 'plotting', 'complex functions',
            '2 parameter functions']


INSTALL_REQUIRES = [
    'numpy (>=1.0.0)',
    'scipy',
    'matplotlib (>=1.5)']


metadata = dict(
    name='colormap2d',
    version=VERSION,
    description='colormap2d',
    long_description=long_description,
    url='https://github.com/MMesch/cmap_builder',
    download_url='https://github.com/MMesch/cmap_builder/zipball/master',
    author='MMesch',
    author_email="MMesch@users.noreply.github.com",
    license='GPL v3',
    keywords=KEYWORDS,
    requires=INSTALL_REQUIRES,
    platforms='OS Independent',
    packages=['colormap2d'],
    classifiers=CLASSIFIERS
)


setup(**metadata)
