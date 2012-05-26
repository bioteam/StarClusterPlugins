#!/usr/bin/env python
import os

from starcluster import threadpool
from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log

class ClusterChef(ClusterSetup):
     """Register cluster nodes with a chef server"""
     def __init__(self, chef_server_url, validation_key, run_list):
          self.chef_server_url = chef_server_url
          self.validation_key = open(validation_key, "r").read()
          self.run_list = run_list
          log.debug('chef_server_url = %s' % self.chef_server_url)
          log.debug('run_list = %s' % self.run_list)
          log.debug('validation_key = %s' % self.validation_key)

     def run(self, nodes, master, user, user_shell, volumes):
          for node in nodes:
            log.info('Bootstrapping chef on %s' % node.alias)
            os.chdir("/Users/kraut/chef-repo")
            os.system("knife bootstrap %s -N %s -x ubuntu --sudo -r %s" % (node.dns_name, node.alias, self.run_list))
