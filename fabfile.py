#!/usr/bin/python
# https://www.digitalocean.com/community/tutorials/how-to-use-fabric-to-automate-administration-tasks-and-deployments

from fabric.operations import local as lrun, run
from fabric.api import task
from fabric.state import env
from fabric.contrib.files import append, sed

paccoURL = "https://github.com/pacco-leo/Pacco-test/"
paccoInstallDir = "PaccoTest"  #This Dir should be changed (since it is defined in startMidori.sh)

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

    # Run deployement script on RPI
    scriptsDir = installDir + "/scripts/"
    env.run("python " + scriptsDir + 'install.py')

