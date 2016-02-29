from distutils.core import setup

import sys

import py2exe

sys.path.append('C:\\Python27\\Lib')
sys.path.append('C:\\Python27\\Lib\\site-packages')
sys.path.append('C:\\Python27\\lib')
data_files = []

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
                'py2exe': {
                    'packages':['werkzeug','email.mime','jinja2.ext'],
                    'includes': ['os',
                                 'flask',
                                 'sys'
                                 ]
                            }
                }
)

# setup(
#     name='tranSMART Arborist',
#     version='1.3',
#     description='Graphical tool to help you prepare your data for loading into the tranSMART data warehouse',
#     url='https://github.com/thehyve/transmart-arborist',
#     author='Ward Weistra',
#     author_email='ward@thehyve.nl',
#     license='GNU General Public License V3',
#     console=['runserver.py'],
#     install_requires=['Flask'],
#     options={
#          'py2exe': {
#             # 'packages': [
#             #              'flask',
#             #              'email',
#             #             ],
#             'includes': [
#                          'flask',
#                          'email',
#                          'os',
#                          'sys',
#                          'collections',
#                          'csv',
#                          'werkzeug',
#                          'urllib',
#                          'markupsafe',
#                          'jinja2',
#                          'jinja2.ext',
#                          'email',
#                          'email.message',
#                          'email.mime.multipart',
#                          'email.mime.text',
#                          'email.utils'
#                         ],
#          }
#     }
# )
