# -*- coding=utf-8 -*-
from packages.dnsblock.dnsblock import ingest_old
import click

@click.group()
def dnsblock():
    pass

@dnsblock.command()
@click.option('--url', '-u', help='Select data from DB', required=False)
def count(url=None):
    if url:
        ingest_old.show_count(url)
    else: ingest_old.show_count
    
if __name__ == '__main__':
    dnsblock()
