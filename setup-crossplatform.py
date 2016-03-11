"""
Author: Jochem Bijlard (j.bijlard@gmail.com)
Setuptools and py2app/py2exe build script for transmart-arborist.

To install dependencies for your machine:
    Usage:
        python setup.py install

To build a packaged executable:
    Usage (Mac OS X):
        python setup.py py2app

        Usage (Windows):
        python setup.py py2exe
"""

import sys
import os
import glob
from setuptools import setup, find_packages
# import ez_setup
# ez_setup.use_setuptools()

mainscript = 'runserver.py'
extra_options = {}
# Which directories to take all normal files from, these have to be specified explicitely.
patterns = [
          'static/*',
          'templates/*',
          'static/img/*',
          'static/img/message/*',
          'static/img/tree/*',
          'static/jstree/*',
          'static/jstree/dist/*',
          'static/jstree/dist/themes/*',
          'static/jstree/dist/themes/default/*',
          'static/jstree/dist/themes/default-dark/*',
           ]


def find_data_files(source, target, patterns):
    """Locates the specified data-files and returns the matches
    in a data_files compatible format.

    source is the root of the source data tree.
        Use '' or '.' for current directory.
    target is the root of the target data tree.
        Use '' or '.' for the distribution directory.
    patterns is a sequence of glob-patterns for the
        files you want to copy.
    """
    if glob.has_magic(source) or glob.has_magic(target):
        raise ValueError("Magic not allowed in src, target")
    ret = {}
    for pattern in patterns:
        pattern = os.path.join(source, pattern)
        for filename in glob.glob(pattern):
            if os.path.isfile(filename):
                targetpath = os.path.join(target, os.path.relpath(filename, source))
                path = os.path.dirname(targetpath)
                ret.setdefault(path, []).append(filename)
    return sorted(ret.items())


def osx_app_build_options():
    """
    Collects additional requirements for building a MacOSX packaged executable. Only works on
    OS X and must have py2app manually installed.
    """
    data_files = find_data_files(source=os.getcwd() + '/arborist',
                                 target='',
                                 patterns=patterns)
    py2app_options = {'argv_emulation': True,
                      'packages': ['jinja2',
                                   'flask',
                                   'email',
                                   ],
                      'includes': ['os',
                                   'flask',
                                   'sys',
                                   ],
                      'excludes': ['mime'],
                      }

    extra_options = dict(
         setup_requires=['py2app'],
         app=[mainscript],
         options={'py2app': py2app_options},
         data_files=data_files,
         )
    return extra_options


def win32_exe_build_options():
    """
    This collects additional requirements for building a Windows executable.
    only works when running from Windows and having manually
    installed the py2exe package.
    """
    import py2exe
    data_files = find_data_files(source=os.getcwd() + r'/arborist',
                                 target='',
                                 patterns=patterns)
    py2exe_options = {'packages': ['werkzeug',
                                   'email.mime',
                                   'jinja2',
                                   ],
                      'includes': ['os',
                                   'flask',
                                   'sys',
                                   'jinja2.ext',
                                   ],
                      }

    extra_options = dict(
        setup_requires=['py2exe'],
        console=[mainscript],
        options={'py2exe': py2exe_options},
        data_files=data_files,
    )


if sys.platform == 'darwin' and 'py2app' in sys.argv:
    extra_options = osx_app_build_options()


elif sys.platform == 'win32' and 'py2exe' in sys.argv:
    extra_options = win32_exe_build_options()


setup(
    name='tranSMART Arborist',
    version='1.3',
    description='Graphical tool to help you prepare your data for loading into the tranSMART data warehouse',
    url='https://github.com/thehyve/transmart-arborist',
    author='Ward Weistra',
    author_email='ward@thehyve.nl',
    license='GNU General Public License V3',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask'],
    scripts=[mainscript],
    **extra_options
)
