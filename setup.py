#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 3

import sys
from cx_Freeze import setup, Executable
from os import path

# GUI applications require a different base on Windows (the default is for a
# console application).

path = sys.path
#path = sys.path + [r"C:\Users\thoma\Desktop\LOG\brainMapper"]
#print(path)

# Dependencies are automatically detected, but it might need fine tuning.
#'./UI/mainView.py'
#("C:\Users\thoma\Desktop\LOG\brainMapper/UI/resources.py","C:\Users\thoma\Desktop\LOG\brainMapper\build\exe.win-amd64-2.7\lib\resources.py")
includefiles = ["UI.bat","mkl_intel_thread.dll",'./ressources']
includes = ["os","sys","time","csv","nibabel","numpy","scipy","sklearn","PyQt4.QtCore", "PyQt4.QtGui",
"pyqtgraph.opengl", "sip", "pyqtgraph.graphicsItems", "atexit","pyqtgraph.debug","numpy.core._methods",
"numpy.lib.format", "scipy.sparse.csgraph._validation","sklearn.tree._criterion","scipy.ndimage._ni_support",
"scipy.ndimage._ni_docstrings","pyqtgraph.ThreadsafeTimer","OpenGL.platform.win32","pyqtgraph.opengl.shaders",
"pyqtgraph.opengl.glInfo","OpenGL.platform.glx","OpenGL.platform.darwin"]
excludes = []
packages = ["UI_builder","clustering_components","ourLib"]
#zip_includes= ["BrainMapper.pyc","./UI/mainView.pyc","./UI/resources.pyc"]
zip_includes =["BrainMapper.pyc"]
#"./UI/clusteringView.pyc","./UI/editCollectionsView.pyc","./UI/exportView.pyc","./UI/calculationView.pyc",
#d = dirname(dirname(abspath(__file__)))
#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

#zip_include_packages= ["../UI","clustering_components"]
#zip_include_packages= ["clustering_components","./UI/UI_builder"]
zip_include_packages=[]
zip_exclude_packages=[]



if sys.platform == "win32":
    pass
elif sys.platform == "linux2":
    pass
else:
    pass

# pour que les bibliotheques binaires de /usr/lib soient recopiees aussi sous Linux
binpathincludes = []
if sys.platform == "linux2":
    binpathincludes += ["/usr/lib"]
 
# niveau d'optimisation pour la compilation en bytecodes
optimize = 0

# si True, n'affiche que les warning et les erreurs pendant le traitement cx_freeze
silent = False

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
    #icone = "brain.png"


cible_1 = Executable(
    script="UI.py",
    base=base,
    #compress=False,  # <= ne pas generer de fichier zip
    #copyDependentFiles=True,
    #appendScriptToExe=True,
    #appendScriptToLibrary=False,  # <= ne pas generer de fichier zip
    #icon=icone
    )

setup(  name = "BrainMapper",
        version = "0.1",
        description = "Executable version of BrainMapper",
        options = {'build_exe': options}, 
        executables = [cible_1])

#Executable("./UI/UI.py", base=base)

# def find_data_file(filename):
#     if getattr(sys, 'frozen', False):
#         # The application is frozen
#         datadir = os.path.dirname(sys.executable)
#     else:
#         # The application is not frozen
#         # Change this bit to match where you store your data files:
#         datadir = os.path.dirname(__file__)

#     return os.path.join(datadir, filename)