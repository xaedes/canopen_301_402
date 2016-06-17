#!/usr/bin/env python

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages=['canopen_301_402',"brave_new_world"],
    package_dir={'': 'src'},
    ##  don't do this unless you want a globally visible script
    # scripts=['bin/myscript'],
    requires=["flufl.enum"]
)

setup(**d)

