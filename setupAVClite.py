from distutils.core import setup
import py2exe, sys, os

setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    windows = [
               {
                'script': "avclite.py",
                 "icon_resources": [(1, "avc_icone.ico")]
              }
              ], 
    zipfile = None,
)