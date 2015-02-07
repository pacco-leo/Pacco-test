#!/usr/bin/python


import os.path
from os.path import *

sudoPassword = 'raspberry'

##paccoInstallDir = join( abspath(join(dirname(abspath(__file__)), os.pardir)), '')
systemScriptsDir = join(dirname(abspath(__file__)),"system/")


#os.path.dirname(os.path.abspath(__file__))


#os.getenv("HOME")

echo "Copying modified config.txt to /boot/"
file1 = systemScriptsDir  + "config.txt"
command1 = "cp " + file1 + " /boot/"
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command1))

echo "Copying startup script (startMidori.sh) to $HOME"
file2 = systemScriptsDir  + "startMidori.sh"
command2 = "cp " + file1 + " /boot/"
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command1))


echo "Copying modified rc.local to /etc"
file3 = systemScriptsDir  + "rc.local"
command3 = "cp " + file1 + " /etc/"
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command1))
