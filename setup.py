#from distutils.core import setup
from setuptools import setup


setup(name='qhpyccd',
      version="0.1",
      description='Python wrapper for the QHYCCD library',
      author='Emmanuel Bertin (IAP / SorbonneU)',
      author_email='bertin@iap.fr',
      setup_requires=["cffi>=1.0.0"],
      install_requires=["cffi>=1.0.0"],
      cffi_modules=["qhpyccd/qhpyccd.py:ffibuilder"],
      packages=['qhpyccd'],
      )

