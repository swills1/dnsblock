# -*- coding=utf-8 -*-
from dnsblock import data
import click

@click.group()
def dnsblock():
    pass

@dnsblock.command()
@click.option('--url', '-u', help='Select data from DB', required=False)
def count(url=None):
    ch = data.CountHosts()
    if url:
        ch.show_count(url)
    else: ch.show_count()
    
if __name__ == '__main__':
    dnsblock()
