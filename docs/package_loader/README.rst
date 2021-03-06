PackageLoader Details
---------------------

Author: Austin Godber <godber 'at' uberhip.com>

**PackageLoader** will check for the file /home/.starcluster-packages and then
load the files recorded there.  In order for this to work, the user must only
install packages on the cluster using the associated *cluster-install*
utility.  This is an *apt-get* wrapper that will install the requested
packages on all nodes and then records them in the appropriate place.

PackageLoader Usage
-------------------

**WARNING** - There are currently issues with how this is implemented.  The main
problems being that when the plugin runs it upgrades any old packages while it
is installing the missing packages.

Until I actually get this packaged as a Python module, you can just drop the
packages.py into your ~/.starclusters/plugins directory and then add a plugin
section to your starcluster config file as shown here::

  [plugin packageloader]
  setup_class = packages.PackageLoader

and then in the clusters you want to add::

  PLUGINS = packageloader

Then copy the *cluster-install* script to the master node.  When installing
packages, do so on the master, as root, with this script.  For example::

  # cluster-install r-recommended ack-grep

Todo
====

 * Resolve upgrade issues with ``PackageLoader``.  As AMIs age it will
   significantly increase cluster startup time.

 * Make the plugin copy ``cluster-install`` to the master node.
