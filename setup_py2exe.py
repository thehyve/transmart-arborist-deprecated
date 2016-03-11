from distutils.core import setup

import sys
import os
# glob will help us search for files based on their extension or filename.
import glob
import py2exe

sys.path.append(r'C:\Python27\Lib')
sys.path.append(r'C:\Python27\Lib\site-packages')
sys.path.append(r'C:\Python27\lib')


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

# Where to start looking for static files
static_source = r'C:\Users\IEUser\python_stuff\arborist\transmart-arborist\arborist\\'
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

py2exe_options = {'packages': ['werkzeug',
                               'email.mime',
                               'jinja2'
                               ],
                  'includes': ['os',
                               'flask',
                               'sys',
                               'jinja2.ext'
                               ],
                  }

setup(
      name='tranSMART Arborist',
      version='1.3',
      description='Graphical tool to help you prepare your data for loading into the tranSMART data warehouse',
      url='https://github.com/thehyve/transmart-arborist',
      author='Ward Weistra',
      author_email='ward@thehyve.nl',
      license='GNU General Public License V3',
      console=['runserver.py'],
      options={
                'py2exe': {py2exe_options

                },
      data_files=data_files
)
