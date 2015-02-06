#!/usr/bin/python
#https://www.digitalocean.com/community/tutorials/how-to-use-fabric-to-automate-administration-tasks-and-deployments


# Fabfile to:
#    - update the remote system(s) 
#    - download and install an application

# Import Fabric's API module
from fabric.api import *


#env.hosts = [
#    'localhost',
  # 'ip.add.rr.ess
  # 'server2.domain.tld',
#]
# Set the username
#env.user   = "root"

# Set the password [NOT RECOMMENDED]
# env.password = "passwd"

def update_upgrade():
    """
        Update the default OS installation's
        basic default tools.
                                            """
    run("aptitude    update")
    run("aptitude -y upgrade")

def install_memcached():
    """ Download and install memcached. """
    run("ls")
	#    run("aptitude install -y memcached")

def update_install():

    # Update
    update_upgrade()

    # Install
    install_memcached()
