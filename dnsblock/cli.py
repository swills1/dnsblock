# -*- coding=utf-8 -*-
from dnsblock import data
import click


@click.group()
def dnsblock():
    pass


@dnsblock.command()
@click.option('--url', '-u', help='Count the entries for blocklists in a list', required=False)
def count(url: str=None):
    """Shows the number of entries and sum total for each url in the blocklist.txt.
    
    :param url: (optional) List of custom urls to count and sum
    """
    counthosts = data.CountHosts()
    if url:
        counthosts.show_count(url)
    else: counthosts.show_count()


@dnsblock.command()
def build():
    """Build a zone file on demand using values in config file."""
    data.build_zone_file_toml()


if __name__ == '__main__':
    dnsblock()
    