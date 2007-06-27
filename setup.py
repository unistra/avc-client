
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



