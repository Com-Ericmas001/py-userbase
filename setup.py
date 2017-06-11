import os
from setuptools import setup, find_packages

# Get __version__ which is stored in src/version.py
ver_file = os.path.join('py_userbase', 'version.py')
exec(open(ver_file).read())

setup(
    name='py_userbase',
    version=__version__,
    packages=find_packages(),
    namespace_packages=['py_userbase'],
    url='',
    license='',
    author='ericmas001',
    author_email='ericmas001@gmail.com',
    description=''
)
