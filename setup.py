import os
import setuptools

import pprp

_APP_PATH = os.path.dirname(pprp.__file__)

with open(os.path.join(_APP_PATH, 'resources', 'README.md')) as f:
      long_description = ''.join(f)

with open(os.path.join(_APP_PATH, 'resources', 'requirements.txt')) as f:
      install_requires = list(map(lambda s: s.strip(), f))

description = \
      "A pure-Python Rijndael (AES) and PBKDF2 library. Python 2.7 and " \
      "Python3 compatible."

setuptools.setup(
      name='pprp',
      version=pprp.__version__,
      description=description,
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[],
      keywords='rijdael pbkdf2',
      author='Dustin Oprea',
      author_email='myselfasunder@gmail.com',
      url='https://github.com/dsoprea/RijndaelPbkdf',
      license='GPL 2',
      packages=setuptools.find_packages(exclude=[]),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      package_data={
            'pprp': [
                  'resources/README.md',
                  'resources/requirements.txt'
            ],
      },
      scripts=[
      ],
)
