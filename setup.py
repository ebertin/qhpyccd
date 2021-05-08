<<<<<<< HEAD
from setuptools import setup
#from distutils.core import setup
=======
#from distutils.core import setup
from setuptools import setup
>>>>>>> f76651e (for some reason distutils is not working on this machine, switch to setup_tools)

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

