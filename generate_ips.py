#!/usr/bin/env python

from netaddr import IPNetwork
import sys

ip_address=str(sys.argv[1])
for ip in IPNetwork(ip_address):
    print '%s' % ip 
