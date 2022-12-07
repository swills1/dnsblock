dnsblock
========
*place-holder*

Overview
--------
This is a Python library used to automatically generate zone files from maintained *Blocklists*.

The overall intent is to have one library that can generate zone files tailored to different resolver software.

It can generate zone files formatted to work with your specific recursive or stub resolver.

Examples would be Unbound or Dnsmaq.

What's the point?
-----------------
Blocklists are curated lists of hosts you may want to block on your local network.

Blocklists are maintained and updated regularly.

Dnsblock allows you to schedule pulling down blocklists as they change, rebuilding your zone file, and restarting 
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

The above code generates entries that look like,

.. code-block:: python
    server:
    local-zone: "pixel.ad" refuse
    local-zone: "centro.pixel.ad" refuse
    # ...