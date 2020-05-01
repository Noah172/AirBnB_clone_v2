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


def do_deploy(archive_path):
    if not path.exists(archive_path) or (
                                        path.exists(archive_path) and
                                        path.isdir(archive_path)):
        return False
    try:
        put(archive_path, '/tmp/')
        name_file_ext = archive_path.split("/")[1]
        name_file = name_file_ext.split(".")[0]
        cmd_mkdir = 'mkdir -p /data/web_static/releases/{}'.format(name_file)
        sudo(cmd_mkdir)
        cmd_uncom = 'tar -xzf /tmp/{}'.format(name_file_ext)
        cmd_uncom += ' -C /data/web_static/releases/{}'.format(name_file)
        sudo(cmd_uncom)
        cmd_rm_file = 'rm /tmp/{}'.format(name_file_ext)
        sudo(cmd_rm_file)
        cmd_mv = 'mv /data/web_static/releases/'
        cmd_mv += '{}/web_static/*'.format(name_file)
        cmd_mv += ' /data/web_static/releases/{}/'.format(name_file)
        sudo(cmd_mv)
        cmd_rm_dir = 'rm -rf /data/web_static/releases/{}'.format(name_file)
        cmd_rm_dir += '/web_static'
        sudo(cmd_rm_dir)
        sudo('rm -rf /data/web_static/current')
        cmd_cre_sym = 'ln -s /data/web_static/releases/{}/'.format(name_file)
        cmd_cre_sym += ' /data/web_static/current'
        sudo(cmd_cre_sym)
        print("New version deployed!")
        return True
    except Exception:
        return False
