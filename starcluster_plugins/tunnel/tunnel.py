#!/usr/bin/env python
import posixpath
import os

from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log

class ClusterTunnel(ClusterSetup):
     """Create ssh tunnel to the master node"""
     def __init__(self, tunnel_port):
          self.tunnel_port = tunnel_port
          log.debug('tunnel_port = %s' % tunnel_port)
     def run(self, nodes, master, user, user_shell, volumes):
	      user_home = master.getpwnam(user).pw_dir
	      log.debug('Creating reverse tunnel on port %s' % self.tunnel_port)
	      key_location = master.key_location
	      os.system('ssh -i %s -f root@%s -L %s:%s:%s -N' % (key_location, master.dns_name, self.tunnel_port, master.dns_name, self.tunnel_port))