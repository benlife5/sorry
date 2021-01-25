from distutils.core import setup
import py2exe

setup(
    windows=[
        {
            "script": "sorry.py",
            "icon_resources": [(1, "logo.ico")]
        }
    ]
)
