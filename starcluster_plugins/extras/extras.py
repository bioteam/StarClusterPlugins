#!/usr/bin/env python

from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log

class ClusterExtras(ClusterSetup):
     """Add compile.q and set scheduler interval for SGE"""
     def run(self, nodes, master, user, user_shell, volumes):
	      log.info('Adding compile.q')
	      cmd = "source /opt/sge6/default/common/settings.sh;"
	      cmd += "qconf -sq all.q | sed s/all.q/compile.q/ > /tmp/compile.q.txt;"
	      cmd += "qconf -Aq /tmp/compile.q.txt"
	      master.ssh.execute(cmd)
	      log.info('Modifying scheduler interval')
	      cmd = "source /opt/sge6/default/common/settings.sh;"
	      cmd += "qconf -ssconf | sed s/0:0:15/0:0:4/ > /tmp/sched.conf.txt;"
	      cmd += "qconf -Msconf /tmp/sched.conf.txt"
	      master.ssh.execute(cmd)
	      log.info('Adding %s to manager list' % user)
	      master.ssh.execute("source /opt/sge6/default/common/settings.sh; qconf -am %s" % user)
	      log.info('Modifying orte parallel environment')
	      cmd = "source /opt/sge6/default/common/settings.sh;"
	      cmd += "qconf -sp orte | sed 's/\/bin\/true/NONE/' > /tmp/orte.txt;"
	      cmd += "qconf -Mp /tmp/orte.txt"
	      master.ssh.execute(cmd)