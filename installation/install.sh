#!/bin/bash

A=`which python3`
dirpython=`echo "${A%p*}"`
dirpackage=`pip3 show pip | grep "Location" | grep -oE "[^ ]+$"`

brew install qt@4

#install sip
curl -L -O https://sourceforge.net/projects/pyqt/files/sip/sip-4.19.13/sip-4.19.13.tar.gz
tar -xvf sip-4.19.13.tar.gz
cd sip-4.19.13
Python3 configure.py -b ../temp_sip -v ../temp_sip -d ../temp_sip -e ../temp_sip
make install
cd ..

#install pyqt4
curl -L -O https://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.12/PyQt4_gpl_mac-4.12.tar.gz
tar -xvf PyQt4_gpl_mac-4.12.tar.gz
QMAKESPEC=unsupported/macx-clang-libc++
cd PyQt4_gpl_mac-4.12
python3 configure-ng.py --sip ../temp_sip/sip --no-stubs --bindir $dirpython  --destdir $dirpackage --sip-incdir=../temp_sip 
make install

cd ../temp_sip
cp sip.so $dirpackage
cp -r sip-4.19.13.dist-info $dirpackage
cd ..


python3 -m pip install -r requirement.txt
python3 -m pip install scipy==1.1.0
python3 -m pip install tensorflow==1.5.0
