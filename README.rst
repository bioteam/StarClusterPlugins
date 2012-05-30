StarCluster-Plugins
===================

This project provides a place to collect user-contributed StarCluster plugins 

Plugins
-------

The following plugins are included in this package:

 * Chef - Registers cluster nodes with a chef-server. Depends on a local knife
   installation
 * Extras - Example modifying SGE settings (adds queue, sets scheduler interval)
 * Gluster - Install/configure GlusterFS on the ephemeral disks
 * Hadoop - Install/configure hadoop
 * Keys - Copy an SSH private key to the master node
 * Mpich - Install/configure mpich
 * Mysql - Install/configure mysql cluster
 * PackageLoader - Loads packages recorded in /home/.starcluster-packages on
   all nodes.
 * Sync - Recursively copy a local directory to the master
 * Tunnel - Create SSH tunnel for port forwarding
 * Xvfb - Installs, configures, and sets up an Xvfb server

License and Copyright
=====================

This program is distributed under the terms of the Lesser GNU General Public
License

Contributors
============

 * Austin Godber <godber 'at' uberhip.com>
 * Adam Marsh
 * Adam Kraut <adam 'at' bioteam.net>
