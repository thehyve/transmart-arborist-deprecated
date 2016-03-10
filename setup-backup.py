from setuptools import setup, find_packages
import sys

for pathpart in ['', '/Users/wardweistra/tools/transmart-arborist/venv/lib/python27.zip', '/Users/wardweistra/tools/transmart-arborist/venv/lib/python2.7', '/Users/wardweistra/tools/transmart-arborist/venv/lib/python2.7/plat-darwin', '/Users/wardweistra/tools/transmart-arborist/venv/lib/python2.7/plat-mac', '/Users/wardweistra/tools/transmart-arborist/venv/lib/python2.7/plat-mac/lib-scriptpackages', '/Users/wardweistra/tools/transmart-arborist/venv/lib/python2.7/lib-tk', '/Users/wardweistra/tools/transmart-arborist/venv/lib/python2.7/lib-old', '/Users/wardweistra/tools/transmart-arborist/venv/lib/python2.7/lib-dynload', '/usr/local/Cellar/python/2.7.9/Frameworks/Python.framework/Versions/2.7/lib/python2.7', '/usr/local/Cellar/python/2.7.9/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-darwin', '/usr/local/Cellar/python/2.7.9/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-tk', '/usr/local/Cellar/python/2.7.9/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-mac', '/usr/local/Cellar/python/2.7.9/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-mac/lib-scriptpackages', '/Users/wardweistra/tools/transmart-arborist/venv/lib/python2.7/site-packages']:
    sys.path.append(pathpart)

print sys.path

PKGS = ['jinja2', 'flask']
INCLUDES = ['os', 'flask', 'sys']
OPTIONS = {'argv_emulation': True,
 'packages': PKGS,
 'includes': INCLUDES
 }

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
    # install_requires=PKGS,
    setup_requires=['py2app'],
    app=['runserver.py'],
    options={'py2app':OPTIONS}
)
