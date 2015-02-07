#!/usr/bin/python


import os.path
from os.path import *

sudoPassword = 'raspberry'

##paccoInstallDir = join( abspath(join(dirname(abspath(__file__)), os.pardir)), '')
systemScriptsDir = join(dirname(abspath(__file__)),"system/")


#os.path.dirname(os.path.abspath(__file__))


#os.getenv("HOME")

echo "Adding "
command1 = "cp " + file1 + " /boot/"
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command1))

echo "Copying modified config.txt to /boot/"
file2 = systemScriptsDir  + "config.txt"
command2 = "cp " + file2 + " /boot/"
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command2))

echo "Copying startup script (startMidori.sh) to $HOME"
file3 = systemScriptsDir  + "startMidori.sh"
command3 = "cp " + file3 + " /boot/"
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command3))


echo "Copying modified rc.local to /etc"
file4 = systemScriptsDir  + "rc.local"
command4 = "cp " + file4 + " /etc/"
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command4))

