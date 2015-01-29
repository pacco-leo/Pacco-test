#!/usr/bin/python
# https://www.digitalocean.com/community/tutorials/how-to-use-fabric-to-automate-administration-tasks-and-deployments

from fabric.operations import local as lrun, run
from fabric.api import task
from fabric.state import env
from fabric.contrib.files import append, sed

paccoURL = "https://github.com/pacco-leo/Pacco-test/"
paccoInstallDir = "PaccoTestTEST"

@task
def localhost():
    env.run = lrun
    env.hosts = ['localhost']


@task
def remote():
    env.run = run
    #env.hosts = ['some.remote.host']
    env.hosts = ['192.168.2.2']
    env.user = "pi"
    env.password = "raspberry"


@task
def install():
    import os
    #homeDir = os.getenv("HOME") #Crappy hack. Try to do it with Fabric
    #homeDir = env.run('echo $HOME')
    homeDir = "/home/pi"

    installDir = homeDir + "/" + paccoInstallDir   #To change on final version
    print "Installing to:" + installDir

    env.run('mkdir -p ' + installDir )

    #env.run('git clone ' + paccoURL + ' ' + installDir)  #DEBUG: Reactivate

    #------------------------------------------------
    #---- Create and copy VideoConfig script (to get fullscreen and no Desktop at startup)

    #http://docs.fabfile.org/en/latest/api/contrib/files.html
    #videoConfigFile = "/boot/config.txt"   #REAL ONE
    videoConfigFile = "/tmp/config.txt"  #JUST FOR DEBUGGING
    #env.run('sudo touch ' + videoConfigFile )
    #env.run('sudo cat ' + '"disable_overscan=1"' + " >> " +  videoConfigFile)
    append(videoConfigFile, "disable_overscan=1", use_sudo=True, partial=False, escape=True, shell=False)
    append(videoConfigFile, "framebuffer_width=800", use_sudo=True, partial=False, escape=True, shell=False)
    append(videoConfigFile, "framebuffer_height=450", use_sudo=True, partial=False, escape=True, shell=False)
    append(videoConfigFile, "framebuffer_depth=32", use_sudo=True, partial=False, escape=True, shell=False)
    append(videoConfigFile, "framebuffer_ignore_alpha=1", use_sudo=True, partial=False, escape=True, shell=False)
    append(videoConfigFile, "hdmi_pixel_encoding=1", use_sudo=True, partial=False, escape=True, shell=False)
    append(videoConfigFile, "hdmi_group=2", use_sudo=True, partial=False, escape=True, shell=False)


    #------------------------------------------------
    #---- Create and copy Midori script (to run browser at startup)
    # TODO : EVITER QUE LE TRUC S AJOUTE A CHAQUE FOIS QU ON RELANCE
    startMidoriScript="""
    #!/bin/sh
    xset -dpms     # disable DPMS (Energy Star) features.
    xset s off       # disable screen saver
    xset s noblank # don't blank the video device
    # python /home/pi/Desktop/Django/PT/manage.py runserver # start Django server
    unclutter &
    matchbox-window-manager &
    midori -e Fullscreen -a http://localhost:8000/paccotest/ouverture/ """

    MidoriFile = homeDir + "/" + "startMidori"
    append(MidoriFile, startMidoriScript, use_sudo=False, partial=False, escape=True, shell=False)


    #------------------------------------------------
    #---- Add MidoriScript to startup script
    #---- Remove "exit 0"  and add
    StartupFile = "/tmp/testRC.local"

    LinesAdd = """
    sudo xinit ./home/pi/startMidori &

    exit 0"""

    sed("/tmp/testRC.local", "exit 0", LinesAdd, limit='', use_sudo=False, backup='.bak', flags='', shell=False)