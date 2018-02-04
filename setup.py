from distutils.core import setup
from setuptools import Extension
import sys
import logging

logging.basicConfig()
log = logging.getLogger()

try:
    from Cython.Distutils import build_ext
    ext_modules = [Extension("jenks", ["jenks.pyx"])]
except ImportError:
    from setuptools.command.build_ext import build_ext
    ext_modules = [Extension("jenks", ["jenks.c"])]


class CustomBuildExtCommand(build_ext):
    """build_ext command for use when numpy headers are needed."""
    def run(self):
        # Import numpy here, only when headers are needed
        try:
            import numpy
        except ImportError:
            log.critical("Numpy is required to run setup(). Exiting.")
            sys.exit(1)
        # Add numpy headers to include_dirs
        self.include_dirs.append(numpy.get_include())
        # Call original build_ext command
        build_ext.run(self)


setup(
    name="jenks",
    version="1.0",
    author="Matthew Perry",
    author_email="perrygeo@gmail.com",
    description=("Cython implementation of jenks natural breaks algorithm"),
    license="BSD",
    keywords="gis geospatial geographic statistics numpy cython choropleth",
    url="https://github.com/perrygeo/jenks",
    install_requires=['numpy', 'cython'],
    setup_requires=['numpy', 'cython'],
    cmdclass={'build_ext': CustomBuildExtCommand},
    ext_modules=ext_modules
)
