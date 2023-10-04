#!/usr/bin/python3
"""
Fabric script to distribute an archive to your web servers
"""
from fabric.api import env, put, run, local
from os.path import exists
env.hosts = ['<IP web-01>', '<IP web-02>']


def do_deploy(archive_path):
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on the server
        put(archive_path, '/tmp')

        # Extract the archive to /data/web_static/releases/
        archive_name = archive_path.split('/')[-1]
        folder_name = archive_name.split('.')[0]
        release_path = '/data/web_static/releases/' + folder_name
        run('mkdir -p {}'.format(release_path))
        run('tar -xzf /tmp/{} -C {}'.format(archive_name, release_path))

        # Delete the archive from the server
        run('rm /tmp/{}'.format(archive_name))

        # Move the files out of the release folder
        run('mv {}/web_static/* {}'.format(release_path, release_path))

        # Remove the empty web_static folder
        run('rm -rf {}/web_static'.format(release_path))

        # Update the symbolic link
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(release_path))
        return True
    except Exception:
        return False

