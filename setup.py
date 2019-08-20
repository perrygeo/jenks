import logging
import sys

logging.basicConfig()
log = logging.getLogger()

try:
    import Cython
except ImportError:
    log.critical(
        "Cython is required to run setup(). Exiting.")
    sys.exit(1)
else:
    from Cython.Distutils import build_ext

from setuptools import setup
from distutils.extension import Extension

include_dirs = []

try:
    import numpy
    include_dirs.append(numpy.get_include())
except ImportError:
    log.critical(
        "Numpy and its headers are required to run setup(). Exiting.")
    sys.exit(1)

setup(
    name="jenks",
    version="1.0",
    author="Matthew Perry",
    author_email="perrygeo@gmail.com",
    description=("Cython implementation of jenks natural breaks algorithm"),
    license="BSD",
    keywords="gis geospatial geographic statistics numpy cython choropleth",
    url="https://github.com/perrygeo/jenks",
    install_requires=['Numpy'],
    cmdclass={'build_ext': build_ext},
    ext_modules = [
        Extension("jenks", ["jenks.pyx"], include_dirs=include_dirs)]
)
