#!/usr/bin/python


import os.path
from os.path import *

sudoPassword = 'raspberry'

# #paccoInstallDir = join( abspath(join(dirname(abspath(__file__)), os.pardir)), '')
systemScriptsDir = join(dirname(abspath(__file__)), "system/")


#os.path.dirname(os.path.abspath(__file__))


#os.getenv("HOME")

print "Adding needed libs"
command1 = "apt-get install matchbox-window-manager"
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command1))

print "Copying modified config.txt to /boot/"
file2 = systemScriptsDir + "config.txt"
command2 = "cp " + file2 + " /boot/"
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command2))

print "Copying startup script (startMidori.sh) to $HOME"
file3 = systemScriptsDir + "startMidori.sh"
command3 = "cp " + file3 + " /boot/"
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command3))

print "Copying modified rc.local to /etc"
file4 = systemScriptsDir + "rc.local"
command4 = "cp " + file4 + " /etc/"
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command4))

