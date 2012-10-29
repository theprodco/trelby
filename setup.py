# setup.py
from distutils.command.build_scripts import build_scripts as _build_scripts
from distutils.command.bdist_rpm import bdist_rpm as _bdist_rpm
from distutils.core import setup
from distutils.util import convert_path

import fileinput
import glob
import sys
import os.path

class build_scripts(_build_scripts):
    """build_scripts command

    This specific build_scripts command will modify the bin/trelby script
    so that it contains information on installation prefixes afterwards.
    """

    def copy_scripts(self):
        _build_scripts.copy_scripts(self)

        if "install" in self.distribution.command_obj:
            iobj = self.distribution.command_obj["install"]
            libDir = iobj.install_lib

            if iobj.root:
                libDir = libDir[len(iobj.root):]

            script = convert_path("bin/trelby")
            outfile = os.path.join(self.build_dir, os.path.basename(script))

            # abuse fileinput to replace a line in bin/trelby
            for line in fileinput.input(outfile, inplace = 1):
                if """sys.path.insert(0, "src")""" in line:
                    line = """sys.path.insert(0, "%s/src")""" % libDir

                print line,

class bdist_rpm(_bdist_rpm):
    """bdist_rpm command

    This specific bdist_rpm command generates an RPM package that
    will install to /usr/share/trelby and /usr/bin, respectively.
    """
    def _make_spec_file(self):
        specFile = _bdist_rpm._make_spec_file(self)
        line = next(i for i, s in enumerate(specFile) if s.startswith("%install"))
        specFile[line+1] += " --prefix=/usr --install-data=/usr/share/trelby --install-lib /usr/share/trelby"
        return specFile

sys.path.append(os.path.join(os.path.split(__file__)[0], "src"))
import misc

includes = [
    "encodings",
    "encodings.*",
    "lxml._elementpath"
]

Plist = dict(CFBundleDocumentTypes=[dict(CFBundleTypeExtensions=["trelby"],
                                         CFBundleTypeName="Trelby Document",
                                         CFBundleTypeRole="Editor",
                                         CFBundleTypeIconFile="icon256.icns",
                                         CFBundleName="Trelby"),
                                   ]
            )

options = {
    "py2exe": {
        "compressed": 1,
        "optimize": 2,
        "includes": includes,
    },
    "py2app": {
         "compressed": 1,
         "optimize": 2,
         "includes": includes,
         'argv_emulation': True,
         'iconfile':'icon256.icns',
         'plist': Plist,
         'includes': includes,
         'packages':['src'],
    }
}

if sys.platform == "win32":
    import py2exe

    platformOptions = dict(
        zipfile = "library.zip",

        windows = [{
                "script" : "bin/trelby",
                "icon_resources": [(1, "icon32.ico")],
           }]
        )
elif sys.platform == "darwin":
    import py2app
    import shutil
    # py2app requires that the runnable file end in .py
    # It cannot be named trelby.py as that name is taken.
    # This name is also used in native Hide and Quit menus.
    shutil.copyfile("bin/trelby","bin/mactrelby.py")
    platformOptions = dict(
         setup_requires = ['py2app'],
          app = ['bin/mactrelby.py'],
    )
else:
    platformOptions = {}

dataFiles = [
    ("resources", glob.glob(os.path.join("resources", "*.*"))),

    ("", ["names.txt.gz",
          "dict_en.dat.gz",
          "sample.trelby",
          "fileformat.txt",
          "manual.html",
          "README",
          ]),
    ]

setup(
    name = "Trelby",
    cmdclass = {"build_scripts": build_scripts, "bdist_rpm": bdist_rpm},
    version = misc.version,
    description = "Free, multiplatform, feature-rich screenwriting program",

    long_description = """\
Trelby is a simple, powerful, full-featured, multi-platform program for
writing movie screenplays. It is simple, fast and elegantly laid out to
make screenwriting simple, and it is infinitely configurable.

Features:

 * Screenplay editor: Enforces correct script format and pagination,
   auto-completion, and spell checking.
 * Multiplatform: Behaves identically on all platforms, generating the exact
   same output.
 * Choice of view: Multiple views, including draft view, WYSIWYG mode,
   and fullscreen to suit your writing style.
 * Name database: Character name database containing over 200,000 names
   from various countries.
 * Reporting: Scene/location/character/dialogue reports.
 * Compare: Ability to compare scripts, so you know what changed between
   versions.
 * Import: Screenplay formatted text, Final Draft XML (.fdx)
    and Celtx (.celtx).
 * Export: PDF, formatted text, HTML, RTF, Final Draft XML (.fdx).
 * PDF: Built-in, highly configurable PDF generator. Supports embedding your
   chosen font. Also supports generating PDFs with custom watermarks,
   to help track shared files.
 * Free software: Licensed under the GPL, Trelby welcomes developers and
   screenwriters to contribute in making it more useful.
""",
      maintainer = "Osku Salerma",
      maintainer_email = "osku.salerma@gmail.com",
      url = "http://www.trelby.org/",
      license = "GPL",
      packages = ["src"],
      data_files = dataFiles,
      scripts = ["bin/trelby"],
      options = options,
      **platformOptions)
