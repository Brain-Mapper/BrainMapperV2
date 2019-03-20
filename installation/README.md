# How to install BrainMapper
If you are not familiar with informatics, we recommend running BrainMapper on Windows or Linux. Since the installation procedure is not automated for MacOS, you may need to adapt the instructions to your own environment.
If the installation doesn't work, we recommend to use the virtual environment method described bellow.

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

### Install python

You need to have python 3.6 to use this project.  

Open the terminal (`Windows+r` and type `cmd`) and type the following line to
check if python is installed

```
python --version
```

If it is installed you should have the following result :

```
Python 3.6.7
```

If the command does not work, it means that python is not installed.  
In this case, you can download it [here](https://www.python.org/downloads/release/python-367/).
During the install, ensure that the options "pip" and "tcl/tk" (on the screen Optional Features),
"add Python to environment variables" (on the screen Advanced Options) are chosen.

You should be able to launch the previous command in a new terminal.

### Install the dependencies

In the command line, install required dependencies with
```
pip install -r <path to>\requirement.txt
```

You also have to download pyqt4 ([here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4), download PyQt4-4.11.4-cp36-cp36m-win_amd64.whl
Then install it with pip

```
pip install <path to>\PyQt4‑4.11.4‑cp36‑cp36m‑win32.whl
```

For example
```
pip install -r C:\Users\Me\BrainMapperV2\installation\Windows\requirement.txt
pip install C:\Users\Me\Downloads\PyQt4-4.11.4-cp36-cp36m-win_amd64.whl
```

### Launch BrainMapper

In the command line, set your current directory at the root of BrainMapper
```
cd <path to>\BrainMapperV2
```

Start the script with python
```
python UI.py
```

For example
```
cd C:\Users\Me\BrainMapperV2
python UI.py
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
$ cd ../temp_sip
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

## Virtual environment
First dowload the virtual environment file folowing this link : https://drive.google.com/a/esial.net/file/d/1gIkC73_cNlArcYdlXNclHnopTxJc7uxj/view?usp=sharing  

Then you need to download the VirtualBox software on your computer :  
MacOS : https://download.virtualbox.org/virtualbox/6.0.4/VirtualBox-6.0.4-128413-OSX.dmg  
Windows : https://download.virtualbox.org/virtualbox/6.0.4/VirtualBox-6.0.4-128413-Win.exe  
Linux : https://download.virtualbox.org/virtualbox/6.0.4/virtualbox-6.0_6.0.4-128413~Ubuntu~bionic_amd64.deb  
(other Linux distributions : https://www.virtualbox.org/wiki/Linux_Downloads)  
Open VirtualBox and click on the "File" menu.  
![Tuto](images/tuto1.png?raw=true "File -> import appliance")  
Click on import appliance and chose BrainMapper.ova. Click on next.  
After the import, you can change the setings or leave the default ones.  
Then you just have to start the machine selected by clicking on the "Start" button.  
The password of the machine is : brainmapper  
To launch the softawe BrainMapper, double click on the "Start.sh" file on the desktop.
