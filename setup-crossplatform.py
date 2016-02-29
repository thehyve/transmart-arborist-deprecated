"""
py2app/py2exe build script for transmart-arborist.

Will automatically ensure that all build prerequisites are available
via ez_setup

Usage (Mac OS X):
    python setup.py py2app

Usage (Windows):
    python setup.py py2exe
"""

import ez_setup
ez_setup.use_setuptools()
import sys
from setuptools import setup, find_packages

# sys.path.append('/Users/wardweistra/tools/transmart-arborist/venv/bin')

mainscript = 'runserver.py'

if sys.platform == 'darwin':
    extra_options = dict(
         setup_requires=['py2app'],
         app=[mainscript],
         # Cross-platform applications generally expect sys.argv to
         # be used for opening files.
        #  options=dict(py2app=dict(argv_emulation=True)),
        #  options={
        #         'py2app': {
        #             'argv_emulation':True,
        #             # 'packages': ['werkzeug','email.mime','jinja2.ext'],
        #             # 'includes': ['os',
        #             #              'flask',
        #             #              'sys',
        #             #              ]
        #                     }
        #         }
    )
elif sys.platform == 'win32':
    extra_options = dict(
        setup_requires=['py2exe'],
        app=[mainscript],
    )
else:
    extra_options = dict(
        # Normally unix-like platforms will use "setup.py install"
        # and install the main script as such
        scripts=[mainscript],
    )

DATA_FILES = []

setup(
    name='tranSMART Arborist',
    version='1.3',
    description='Graphical tool to help you prepare your data for loading into the tranSMART data warehouse',
    url='https://github.com/thehyve/transmart-arborist',
    author='Ward Weistra',
    author_email='ward@thehyve.nl',
    license='GNU General Public License V3',
    data_files=DATA_FILES,
    # packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['jinja2','flask'],
    scripts=['runserver.py'],
    **extra_options
)
