#!/usr/bin/python3
""" Fabric script"""
from fabric.api import task, local, env, run, put
from datetime import datetime
import os

env.hosts = ['52.207.208.21', '54.146.74.86']


@task
def do_pack():
    """Fabric script that generates a .tgz archive"""
    date = datetime.now().strftime('%Y%m%d%H%M%S')
    makefile = "mkdir -p versions"
    t = "versions/web_static_{}.tgz".format(date)
    print("Packing web_static to {}".format(t))
    if local("{} && tar -cvzf {} web_static".format(makefile, t)).succeeded:
        return t
    return None


@task
def do_deploy(archive_path):
    """distributes an archive to your web servers
       using the function do_deploy:"""
    try:
        if not os.path.exists(archive_path):
            return False
        m = os.path.basename(archive_path)
        n, ext = os.path.splitext(m)
        dic = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        run("rm -rf {}{}/".format(dic, n))
        run("mkdir -p {}{}/".format(dic, n))
        run("tar -xzf /tmp/{} -C {}{}/".format(m, dic, n))
        run("rm /tmp/{}".format(m))
        run("mv {0}{1}/web_static/* {0}{1}/".format(dic, n))
        run("rm -rf {}{}/web_static".format(dic, n))
        run("rm -rf /data/web_static/current")
        run("ln -s {}{}/ /data/web_static/current".format(dic, n))
        print("New version deployed!")
        return True
    except Exception:
        return False
