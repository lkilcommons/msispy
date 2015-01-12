# This code is covered under the DavitPy license (GPL v3), which is included with this software
#
# The code was original authored by The VT Superdarn Lab and friends,
# You can get in contact with the original authors via the GitHub
# Original author email: ajribeiro86@gmail.com
# Original Copyright: 2012 VT Superdarn
# 
# I have made only minor modifications to the VT work
# primarily the inclusion of additional test scripts and a validation tool
# my purpose was to increase the modularity of this code so it can get more use.
#
# Liam Kilcommons - University of Colorado, Boulder - Colorado Center for Astrodynamics Research
# December, 2014

import os
import glob

os.environ['DISTUTILS_DEBUG'] = "1"

from setuptools import setup, Extension
from setuptools.command import install as _install
from numpy.distutils.core import setup, Extension

#This is a stripped down version of the setup file for davitpy. I stripped out everything
#except MSIS so that it could be used independantly
# This code is covered under the DavitPy license (GPL v3), which is included with this software

#blah.extensionBlah is the way to specify that you want extensionBlah to be a member of package blah
msisFort = Extension("msispy.msisFort",sources=["msispy/nrlmsise00_sub.for",'msispy/nrlmsis.pyf'])

setup(name='msispy',
      version = "0.1.0",
      description = "The NRLMSISE00 model of the neutral atmosphere",
      #author = "VT SuperDARN Lab and friends",
      #author_email = "ajribeiro86@gmail.com",
      author = "University of Colorado Space Environent Data Analysis Group (CU-SEDA)",
      author_email = 'liam.kilcommons@colorado.edu',
      url = "http://pypi.python.org/pypi/MsisPy",
      download_url = "https://github.com/vtsuperdarn/davitpy/models/msis",
      long_description = "This is a standalone version of the VT SuperDARN Davitpy MSIS (nrlmsise00). All due credit to the original authors.",
      ext_modules = [msisFort],
      install_requires=[],
      packages=['msispy'],
      package_dir={'msispy' : 'msispy'},
      package_data={'msispy': ['apf107.dat']}, #data names must be list
      license='LICENSE.txt',
      zip_safe = False,
      classifiers = [
            "Development Status :: 4 - Beta",
            "Topic :: Scientific/Engineering",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: GNU General Public License (GPL)",
            "Natural Language :: English",
            "Programming Language :: Python"
            ],
      )

# setup(
#     name='TowelStuff',
#     version='0.1.0',
#     author='J. Random Hacker',
#     author_email='jrh@example.com',
#     packages=['towelstuff', 'towelstuff.test'],
#     scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
#     url='http://pypi.python.org/pypi/TowelStuff/',
#     license='LICENSE.txt',
#     description='Useful towel-related stuff.',
#     long_description=open('README.md').read(),
#     install_requires=[
#         "Django >= 1.1.1",
#         "caldav == 0.1.4",
#     ],
# )
