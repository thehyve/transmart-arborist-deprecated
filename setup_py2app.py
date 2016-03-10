from setuptools import setup, find_packages
import sys
import glob
import os

sys.path.append('/Users/jochembijlard/.virtualenvs/arboristenv/lib/python2.7/')
sys.path.append('/Users/jochembijlard/.virtualenvs/arboristenv/lib/python2.7/site-packages/')
sys.path.append('/Users/jochembijlard/.virtualenvs/arboristenv/Lib/')

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
        pattern = os.path.join(source,pattern)
        for filename in glob.glob(pattern):
            if os.path.isfile(filename):
                targetpath = os.path.join(target,os.path.relpath(filename,source))
                path = os.path.dirname(targetpath)
                ret.setdefault(path,[]).append(filename)
    return sorted(ret.items())

# Where to start looking for static files
static_source = '/Users/jochembijlard/projects/transmart-arborist/arborist/'
# Which directories to take all normal files from
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

data_files = find_data_files(source=static_source,
                             target='',
                             patterns=patterns)

PKGS = ['jinja2', 'flask', 'email']
INCLUDES = ['os', 'flask', 'sys']
EXCLUDES = ['mime']
OPTIONS = {'argv_emulation': True,
           'packages': PKGS,
           'includes': INCLUDES,
           'excludes': EXCLUDES,
           }

setup(
    name='tranSMART-Arborist',
    version='1.3',
    description='Graphical tool to help you prepare your data for loading into the tranSMART data warehouse',
    url='https://github.com/thehyve/transmart-arborist',
    author='Ward Weistra',
    author_email='ward@thehyve.nl',
    license='GNU General Public License V3',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    # install_requires=PKGS,
    setup_requires=['py2app'],
    app=['runserver.py'],
    data_files=data_files,
    options={'py2app':OPTIONS}
)
