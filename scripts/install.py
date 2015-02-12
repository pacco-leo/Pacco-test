#!/usr/bin/python
#title           :install.py
#description     :
#author          :paccotest
#date            :20140702
#version         :0.1
#usage           :
#notes           :
#bash_version    :
#==============================================================================

import os.path
from os.path import *

#------- Constants
sudoPassword = 'raspberry'
libs = ["matchbox-window-manager", "python-dev" , "python-pip", "chromium"]
pyLibs = ["Django==1.7", "django-modeltranslation" ]


# #paccoInstallDir = join( abspath(join(dirname(abspath(__file__)), os.pardir)), '')
systemScriptsDir = join(dirname(abspath(__file__)), "system/")


print "Adding needed libs"
for lib in libs:
	command = "apt-get --assume-yes install " + lib
	p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))

print "Adding python libs"
for lib in pyLibs:
        command = "pip install " + lib
        p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))

print "Copying modified config.txt to /boot/"
file2 = systemScriptsDir + "config.txt"
command2 = "cp " + file2 + " /boot/"
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command2))

print "Copying startup script (startPaccoTest.sh) to $HOME"
file3 = systemScriptsDir + "startPaccoTest.sh"
command3 = "cp " + file3 + " " + join(os.getenv("HOME"), '')
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command3))

print "Copying modified rc.local to /etc"
file4 = systemScriptsDir + "rc.local"
command4 = "cp " + file4 + " /etc/"
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command4))

