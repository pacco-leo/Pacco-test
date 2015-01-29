#!/usr/bin/python
#https://www.digitalocean.com/community/tutorials/how-to-use-fabric-to-automate-administration-tasks-and-deployments

from fabric.api import run, sudo, local
from contextlib import contextmanager

@contextmanager
def locally():
    global run
    global sudo
    global local
    _run, _sudo = run, sudo
    run = sudo = local
    yield
    run, sudo = _run, _sudo

def local_task():
    with locally():
        run("ls -la")