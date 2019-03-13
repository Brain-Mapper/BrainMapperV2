# How to install BrainMapper

## Linux
### Install the dependencies
In the Linux folder, launch the installation script :
```shell
$ chmod +x install.sh
$ ./install.sh
```

### Launch BrainMapper
Then you can launch BrainMapper with the following command from the root folder:

```shell
$ python3 UI.py
```

## MacOS
### Install python 3
If python3 is not already install on your computer, you need to download it. Folow this link:
https://www.python.org/ftp/python/3.7.2/python-3.7.2-macosx10.6.pkg

### Install the dependencies
In the MacOS folder, launch the installation script :
```shell
$ chmod +x install.sh
$ ./install.sh
```
This might take a while

### Launch BrainMapper
Then you can launch BrainMapper with the following command from the root folder:

```shell
$ python3 UI.py
```

## Windows
Télécharger le fichier pyqt4 avec la version correspondante à votre version de python: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4

Lancer dans un powershell la commande suivante :
```powershell
pip install C:\path\where\wheel\is\PyQt4-4.11.4-cp36-cp36m-win_amd64.whl  ( cette exemple est fait avec une version de pyqt4 pour python 3.6)
```
