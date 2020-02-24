#!/bin/bash
sudo apt update
sudo apt install python3-pip
if [ $? != 0 ]; then
	exit 1
fi
sudo -H pip3 install -e .
if [ $? != 0 ]; then
	exit 1
fi
pip3 install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-18.04/ wxPython 
if [ $? != 0 ]; then
	exit 1
fi
sudo apt install libsdl1.2debian
if [ $? != 0 ]; then
	exit 1
fi

echo "Installation finished"
