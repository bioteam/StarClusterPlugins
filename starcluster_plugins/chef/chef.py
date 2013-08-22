import json

from starcluster import clustersetup
from starcluster.logger import log

class ChefClient(clustersetup.DefaultClusterSetup):
     """
     Configures chef-client on StarCluster master node

     Example config:
     [plugin chef]
     SETUP_CLASS = chef.ChefClient
     CHEF_SERVER_URL = https://api.opscode.com/organizations/bioteam
     VALIDATION_CLIENT_NAME = bioteam-validator
     VALIDATION_KEY = /Users/kraut/.chef/bioteam-validator.pem
     RUN_LIST = recipe[ohai]

     """
     
     def __init__(self, chef_server_url, validation_client_name, validation_key, run_list):
          self.chef_server_url = chef_server_url
          self.validation_client_name = validation_client_name
          self.validation_key = open(validation_key, 'r').read()
          self.install_sh = 'https://www.opscode.com/chef/install.sh'
          self.run_list = run_list
          log.debug('chef_server_url = %s' % self.chef_server_url)
          log.debug('validation_client_name = %s' % self.validation_client_name)
          # log.debug('validation_key = %s' % self.validation_key)
          log.debug('run_list = %s' % self.run_list)

     def _start_chef(self, node):
          log.info("Starting chef-client")
          node.ssh.execute('chef-client -j /etc/chef/first-boot.json')

     def _first_boot_json(self, node):
          first_boot_json = node.ssh.remote_file('/etc/chef/first-boot.json', 'w')
          first_boot_json.write(json.dumps({'run_list': self.run_list.split(',')}))
          first_boot_json.close()

     def _client_config(self, node):
          log.info("Writing /etc/chef/client.rb")
          client_rb = node.ssh.remote_file('/etc/chef/client.rb')
          client_rb.write('\n'.join([
              "log_level      :auto",
              "log_location   STDOUT",
              "chef_server_url '%s'" % self.chef_server_url,
              "validation_client_name '%s'" % self.validation_client_name,
              ""
          ]))
          client_rb.close()

     def _validation_key(self, node):
          validation_pem = node.ssh.remote_file('/etc/chef/validation.pem')
          validation_pem.write(self.validation_key)

     def _install_chef(self, node):
          log.info("Installing chef")
          if not node.ssh.isfile('/usr/bin/chef-client'):
               node.ssh.execute("wget %s && bash install.sh" % self.install_sh)

     def run(self, nodes, master, user, user_shell, volumes):
          self._install_chef(master)
          self._validation_key(master)
          self._client_config(master)
          self._first_boot_json(master)
          self._start_chef(master)
               