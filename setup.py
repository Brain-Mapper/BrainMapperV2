#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 3

import sys
from cx_Freeze import setup, Executable
from os import path

import cx_Freeze.hooks
def hack(finder, module):
    return
cx_Freeze.hooks.load_matplotlib = hack

# GUI applications require a different base on Windows (the default is for a
# console application).

path = sys.path
#print(path)

# Debug for Aurélien

import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

# Dependencies are automatically detected, but it might need fine tuning.
#'./UI/mainView.py'
#("C:\Users\thoma\Desktop\LOG\brainMapper/UI/resources.py","C:\Users\thoma\Desktop\LOG\brainMapper\build\exe.win-amd64-2.7\lib\resources.py")
includefiles = ["UI.bat",'./ressources',os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),]
includes = ["os","sys","time","csv","nibabel","numpy","scipy","sklearn","sip","atexit","OpenGL","PyQt4","pyqtgraph",
"matplotlib","nilearn","tkinter", "pandas", "tkinter.filedialog",
"mpl_toolkits",
"PyQt4.QtCore", "PyQt4.QtGui",
"pyqtgraph.opengl", "pyqtgraph.graphicsItems","pyqtgraph.debug",
"numpy.core._methods", "numpy.lib.format",
"scipy.sparse.csgraph._validation","scipy.ndimage._ni_support","scipy.ndimage._ni_docstrings",
"sklearn.tree._criterion",
"pyqtgraph.ThreadsafeTimer","pyqtgraph.opengl.shaders",
"pyqtgraph.opengl.glInfo","pyqtgraph.units","pyqtgraph.reload",
"pyqtgraph.PlotData","pyqtgraph.ordereddict","pyqtgraph.frozenSupport","pyqtgraph.configfile",
"OpenGL.arrays._buffers","OpenGL.arrays._strings","OpenGL.arrays.buffers",
"OpenGL.arrays.ctypesarrays","OpenGL.arrays.ctypesparameters","OpenGL.arrays.ctypespointers","OpenGL.arrays.lists",
"OpenGL.arrays.nones","OpenGL.arrays.numbers","OpenGL.arrays.numpybuffers","OpenGL.arrays.numpymodule",
"matplotlib.backends.backend_tkagg"]
#conflit de nom entre scipy.spatial.ckdtree dans les lib et dans le build


excludes = ["scipy.spatial.cKDTree"]
packages = ["UI_builder","clustering_components","ourLib"]
#zip_includes= ["BrainMapper.pyc","./UI/mainView.pyc","./UI/resources.pyc"]
zip_includes =[]
#d = dirname(dirname(abspath(__file__)))
#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
zip_include_packages=[]
zip_exclude_packages=[]


if sys.platform == "win32":
  includes+= ["OpenGL.platform.win32"]
  includefiles+=["mkl_intel_thread.dll"]
elif sys.platform == "linux2":
  includes+= ["OpenGL.platform.glx"]
  includefiles+=[(matplotlib.get_data_path(), "mpl-data")]
else:
  includes+= ["OpenGL.platform.darwin"]

# pour que les bibliotheques binaires de /usr/lib soient recopiees aussi sous Linux
binpathincludes = []
if sys.platform == "linux2":
    binpathincludes += ["/usr/lib"]
    binpathincludes += ["~/.local/lib"]
 
# niveau d'optimisation pour la compilation en bytecodes
optimize = 0

# si True, n'affiche que les warning et les erreurs pendant le traitement cx_freeze
silent = True

# construction du dictionnaire des options
options = {"path": path,
           "includes": includes,
           "excludes": excludes,
           "packages": packages,
           "include_files": includefiles,
           "bin_path_includes": binpathincludes,
           "include_msvcr": True,
           "zip_includes": zip_includes,
           "zip_include_packages": zip_include_packages,
           "zip_exclude_packages": zip_exclude_packages,
           "optimize": optimize,
           "silent": silent,
           }
 
# pour inclure sous Windows les dll system de Windows necessaires
if sys.platform == "win32":
    options["include_msvcr"] = True

# preparation des cibles
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # pour application graphique sous Windows
    # base = "Console" # pour application en console sous Windows
base=None 
icone = None
if sys.platform == "win32":
    icone = "icone.ico"

cible_1 = Executable(
    script="UI.py",
    base=base,
    )

setup(name = "BrainMapper",
      version = "0.1",
      description = "Executable version of BrainMapper",
      options = {'build_exe': options},
      executables = [cible_1])
