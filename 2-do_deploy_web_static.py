#!/usr/bin/python3
""" Fabric script to deploy """
import os
from fabric.api import *
from datetime import datetime

env.hosts = ['35.231.14.240', '34.229.216.161']
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"
env.warn_only = True

def do_deploy(archive_path):
    """ upload to web servers and deploy """
    if not os.path.exists(archive_path) and not os.path.isfile(archive_path):
        return False
    try:
        # get file name without extension
        filename = os.path.splitext(os.path.basename(archive_path))[0]
        # upload to /tmp dir to server
        put(local_path=archive_path, remote_path="/tmp")
        # create destination directory
        run("mkdir -p /data/web_static/releases/" + filename + "/")
        # uncompress tar file to a directory
        run("sudo tar -xzf /tmp/" + filename + ".tgz" +
            " -C /data/web_static/releases/" + filename + "/")
        # Delete file uploaded
        run("rm /tmp/" + filename + ".tgz")

        # move files to a previous folder
        run("mv /data/web_static/releases/" + filename +
            "/web_static/* /data/web_static/releases/" + filename + "/")

        # delete that folder
        run("rm -rf /data/web_static/releases/" + filename +
            "/web_static")

        # delete symbolic link /data/web_static/current
        run("rm -rf /data/web_static/current")
        # create a new symbolic link
        run("ln -s /data/web_static/releases/" + filename +
            "/ /data/web_static/current")
        print("New version deployed!")
        return True
    except:
        return False
