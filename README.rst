dnsblock
========
*place-holder*

Overview
--------
This is a Python library used to automatically generate zone files from maintained *Blocklists*.
The overall intent is to be able to generate zone files tailored to to different pieces of software.
It can generate zone file formatted to work with your specific Rrecursive or stub resolver.
Examples would be Unbound or Dnsmaq.

What's the point?
-----------------
Blocklists are maintained lists of hosts you may want to block on your network. These lists change.
Dnsblock allows you to schedule pulling down blocklists, rebuilding your zone file, and restarting 
your DNS software without you ever having to be involved.

Dnsblock also allows you to ingest multiple blocklists at once.
It works by the user creating a txt file and adding every blocklist they want to make up their zone file.
The library then uses threading to ingest every blocklist and then builds and formats a tailored zone file.

Installation & Documentation
----------------------------

.. code-block:: python

    *place-holder*

Documentation_ can be found at Read the Docs.

.. _Documentation: https://readthedocs.org/projects/dnsblock/

Basic Usage
-----------

.. code-block:: python

    from dnsblock import data
    
    # Build an Unbound zone file to block traffic
    build_conf = data.BuildConf('local-zone: "', '" refuse', '/etc/zone/file')
    build_conf.build_zone_file()