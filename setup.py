from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
setup(
    name="jenks",
    version="1.0",
    author="Matthew Perry",
    author_email="perrygeo@gmail.com",
    description=("Cython implementation of jenks natural breaks algorithm"),
    license="BSD",
    keywords="gis geospatial geographic statistics numpy cython choropleth",
    url="https://github.com/perrygeo/jenks",
    cmdclass={'build_ext': build_ext},
    ext_modules = [Extension("jenks", ["jenks.pyx"])]
)
