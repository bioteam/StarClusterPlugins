#!/usr/bin/env python
import posixpath
import os

from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log

class ClusterSync(ClusterSetup):
    """Copies all files in a specific directory to the users home directory"""
    def __init__(self, sync_dir):
	     self.sync_dir = sync_dir
	     log.debug('sync_dir = %s' % self.sync_dir)
    def run(self, nodes, master, user, user_shell, volumes):
	     user_home = master.getpwnam(user).pw_dir
	     uid = int(master.ssh.execute('id -u %s' % user)[0])
	     gid = int(master.ssh.execute('id -g %s' % user)[0])
	     log.info('Sync %s to %s' % (self.sync_dir, user_home))
	     for (path, dirs, files) in os.walk(self.sync_dir):
		   for f in files:
			  log.info(f)
			  local_file = open(posixpath.join(path, f), 'r')
			  remote_file = master.ssh.remote_file(posixpath.join(user_home, f))
			  remote_file.write(local_file.read())
			  local_file.close()
			  remote_file.chown(uid, gid)
			  remote_file.close()
	     log.info('Sync finished')