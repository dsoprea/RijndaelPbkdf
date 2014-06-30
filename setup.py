import os.path
import setuptools

import pprp

app_path = os.path.dirname(pprp.__file__)

with open(os.path.join(app_path, 'resources', 'README.rst')) as f:
      long_description = ''.join(f)

with open(os.path.join(app_path, 'resources', 'requirements.txt')) as f:
      install_requires = list(map(lambda s: s.strip(), f))

description = "A pure-Python Rijndael (AES) and PBKDF2 library. Python2.7- "\
              "and Python3-compatible."

setuptools.setup(
      name='pprp',
      version=pprp.__version__,
      description=description,
      long_description=long_description,
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
            'pprp': ['resources/README.rst',
                     'resources/requirements.txt'],
      },
      scripts=[
      ],
)
