#!/usr/bin/env python
import posixpath

from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log

class ClusterKeys(ClusterSetup):
     """Copy an ssh private key to the master node"""
     def __init__(self, key_location, key_name):
          self.key_location = key_location
          self.key_name = key_name
          log.debug('key_location = %s' % key_location)
          log.debug('key_name = %s' % key_name)
     def run(self, nodes, master, user, user_shell, volumes):
	      user_home = master.getpwnam(user).pw_dir
	      user_key_location = posixpath.join(user_home, '.ssh', self.key_name)
	      log.info('Copying private key %s to %s' % (self.key_location, user_key_location))
	      f = open(self.key_location, 'r')
	      local_key = f.read()
	      f.close()
	      remote_key = master.ssh.remote_file(user_key_location)
	      remote_key.write(local_key)
	      master.ssh.execute('chown %s:%s %s' % (user, user, user_key_location))
	      remote_key.chmod(0600)
	      remote_key.close()