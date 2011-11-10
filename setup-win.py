################################################################################
# This is the py2exe setup file to create an .exe build 
# for audiovideocours projects.
#
# Usage: python setup.py py2exe
# 
# !!! This setup file works well with py2exe 0.6.6 (not 0.8.8) !!!
#
################################################################################

from distutils.core import setup
import py2exe


setup(windows=['mediacours.py'],
options = {
"py2exe": {
"packages": [ "pywinauto",
"pywinauto.controls", "pywinauto.tests"],

          }
          }
          )



