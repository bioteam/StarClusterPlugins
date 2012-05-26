import os

from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log

class ClusterGluster(ClusterSetup):
	"""
	Installs, creates, and starts a GlusterFS distributed filesystem
	"""
	def __init__(self, volume_name, mount_point):
		self.gluster_deb_url = "http://download.gluster.com/pub/gluster/glusterfs/3.2/3.2.6/Ubuntu/10.04/glusterfs_3.2.6-1_amd64.deb"
		self.volume_name = volume_name
		self.mount_point = mount_point
	
	def _install_gluster(self, master, nodes):
		for node in nodes:
			if not node.ssh.isfile("/usr/sbin/gluster"):
				log.info("Installing glusterfs on %s" % node.alias)
				cmd = "cd /tmp; wget %s;" % self.gluster_deb_url
				cmd += "dpkg -i glusterfs_3.2.6-1_amd64.deb;"
				log.debug(node.ssh.execute(cmd))
		
		for node in nodes:
			if not node.ssh.isfile("/var/run/glusterd.pid"):
				log.info("Starting glusterd on %s" % node.alias)
				cmd = "/etc/init.d/glusterd start"
				log.debug(node.ssh.execute(cmd))
	
	def _probe_peers(self, master, nodes):
		cmd = ""
		log.info("Probing %d nodes" % len(nodes))
		for node in nodes:
			cmd += "/usr/sbin/gluster peer probe %s;" % node.alias
			log.debug(master.ssh.execute(cmd))
		log.debug(master.ssh.execute("/usr/sbin/gluster peer status"))
	
	def _move_mount(self, nodes):
		"""Make the mount points unique so we can use them as bricks"""
		for node in nodes:
			if not node.ssh.isdir("/%s" % node.alias):
				cmd = "umount /mnt; mkdir /%s; sed -i 's/mnt/%s/g' /etc/fstab; mount -a" % (node.alias, node.alias)
				node.ssh.execute(cmd)
	
	def _create_volume(self, master, nodes):
		"""Create a distributed volume"""
		if not master.ssh.isfile("/tmp/.glusterCreated"):
			cmd = "/usr/sbin/gluster volume create %s " % self.volume_name
			for node in nodes:
				cmd += "%s:/%s " % (node.alias, node.alias)
			cmd += "; touch /tmp/.glusterCreated"
			log.info("Creating distributed volume %s" % self.volume_name)
			master.ssh.execute(cmd)
			log.debug(master.ssh.execute("/usr/sbin/gluster volume info"))
			log.info("Starting distributed volume %s" % self.volume_name)
			master.ssh.execute("/usr/sbin/gluster volume start %s" % self.volume_name)
	
	def _mount_volume(self, master, nodes):
		log.info("Mounting %s" % self.volume_name)
		for node in nodes:
			if not node.ssh.isdir(self.mount_point):
				node.ssh.execute("modprobe fuse; mkdir %s; mount -t glusterfs master:/%s %s" % (self.mount_point, self.volume_name, self.mount_point))
	
	def run(self, nodes, master, user, user_shell, volumes):
		self._install_gluster(master, nodes)
		self._probe_peers(master, nodes)
		self._move_mount(nodes)
		self._create_volume(master, nodes)
		self._mount_volume(master, nodes)
	