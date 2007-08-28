################################################################################
# This is the py2exe setup file to create an .exe build 
# for audiovideocours external version projects.
#
# Usage: python setupEX.py py2exe
################################################################################

from distutils.core import setup
import py2exe


setup(windows=['mediacoursEX.py'],
options = {
"py2exe": {
"packages": [ "pywinauto",
"pywinauto.controls", "pywinauto.tests"],

          }
          }
          )



