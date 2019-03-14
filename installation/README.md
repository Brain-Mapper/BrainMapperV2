# How to install BrainMapper
If you are not familiar with informatics, we recommend running BrainMapper on Windows or Linux. Since the installation procedure is not automated for MacOS, you may need to adapt the instructions to your own environment.

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

## Windows
Télécharger le fichier pyqt4 avec la version correspondante à votre version de python: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4

Lancer dans un powershell la commande suivante :
```powershell
pip install C:\path\where\wheel\is\PyQt4-4.11.4-cp36-cp36m-win_amd64.whl  ( cette exemple est fait avec une version de pyqt4 pour python 3.6)
```

## MacOS
### Install python 3
If python3 is not already install on your computer, you need to download it. Folow this link:
https://www.python.org/ftp/python/3.6.5/python-3.6.5-macosx10.9.pkg

### Install the dependencies
Open a terminal in the MacOS folder.
For the installation you will need to note the folders where python3 and python3 dependencies are installed :

_Python3 folder_ :
```shell
$ which python3
```
For exemple if you get /usr/bin/python3, python3 folder is /urs/bin/

_Dependencies folder :_
```shell
$ echo `pip3 show pip | grep "Location" | grep -oE "[^ ]+$"`
```
(for exemple /usr/lib/python3/dist-packages)

Install brew following the official website : https://brew.sh/

Then install Qt4 :

```shell
$ brew tap cartr/qt4
$ brew tap-pin cartr/qt4
$ brew install qt@4
```
Install sip from source:

```shell
$ curl -L -O https://sourceforge.net/projects/pyqt/files/sip/sip-4.19.13/sip-4.19.13.tar.gz
$ tar -xvf sip-4.19.13.tar.gz
$ cd sip-4.19.13
$ python3 configure.py -b ../temp_sip -v ../temp_sip -d ../temp_sip -e ../temp_sip
$ make install
$ cp sip.so <Dependencies folder>
$ cp -r sip-4.19.13.dist-info <Dependencies folder>
$ cd ..
```

Install PyQt4 from source :

```shell
$ curl -L -O https://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.12/PyQt4_gpl_mac-4.12.tar.gz
$ tar -xvf PyQt4_gpl_mac-4.12.tar.gz
$ QMAKESPEC=unsupported/macx-clang-libc++
$ cd PyQt4_gpl_mac-4.12
$ python3 configure-ng.py --sip ../temp_sip/sip --no-stubs --bindir <Python3 folder>  --destdir <Dependencies folder> --sip-incdir=../temp_sip
$ make install
$ cd ..
```
Install other dependencies :

```shell
$ python3 -m pip install -r requirement.txt
$ python3 -m pip install scipy==1.1.0
$ python3 -m pip install tensorflow==1.5.0
```


### Launch BrainMapper
Then you can launch BrainMapper with the following command from the root folder:

```shell
$ python3 UI.py
```
