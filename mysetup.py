from distutils.core import setup
import py2exe
options={
        "py2exe":{
                    "compressed":1,
                    "optimize":2,
                    "bundle_files":2
                 }
        }
setup(
      options=options,
      zipfile=None,
      console=["SZHcube 2.0.py"]
      )
