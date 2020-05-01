#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import *
from os import path
from datetime import datetime
from shlex import split


env.hosts = ['35.231.14.240', '34.229.216.161']


    now = datetime.utcnow()
    file_ = "versions/web_static_{}{}{}{}{}{}.tgz".format(now.year,
            now.month,                                                                                       now.day,
            now.hour,
            now.minute,
            now.second)

    if not path.isdir("versions"):
        if local("mkdir -p versions").failed:
            return None
    if local('tar -cvzf {} web_static'.format(file_)).failed:
        return None
    return file_


def do_deploy(archive_path):

    if not path.isfile(archive_path):
        return False
    file_ = archive_path.split("/")[-1]
    name = file_.split(".")[0]
    tmp = "/tmp/{}".format(file_)
    data = "/data/web_static/releases/{}/".format(name)
    current = "/data/web_static/current"
    if put("0-setup_web_static.sh", "/tmp/").failed:
        return False
    if sudo("chmod u+x /tmp/0-setup_web_static.sh").failed:
        return False
    if sudo("/tmp/0-setup_web_static.sh").failed:
        return False
    if sudo("rm /tmp/0-setup_web_static.sh").failed:
        return False
    if put(archive_path, tmp).failed:
        return False
    if sudo("rm -rf {}".format(data)).failed:
        return False
    if sudo("mkdir -p {}".format(data)).failed:
        return False
    if sudo("tar -xzf {} -C {}".format(tmp, data)).failed:
        return False
    if sudo("rm {}".format(tmp)).failed:
        return False
    if sudo("mv {}web_static/* {}".format(data, data)).failed:
        return False
    if sudo("rm -rf {}web_static".format(data)).failed:
        return False
    if sudo("rm -rf {}".format(current)).failed:
        return False
    if sudo("ln -s {} {}".format(data, current)).failed:
        return False
    print("New version deployed!")

    return True


def deploy():

    archive_path = do_pack()

    if not archive_path:
        return False

    return do_deploy(archive_path)
