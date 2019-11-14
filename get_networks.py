#!/usr/bin/env python
from netaddr import *
import pyping
import argparse, sys

def ping_process(r, ip):
    TGREEN =  '\033[32m'
    ENDC = '\033[m'
    resp = pyping.ping(str(ip))
    if resp.ret_code == 0:
        print(TGREEN + " [*] %s -  %s --> is up " + ENDC) % (r.rstrip('\n'), ip)
    else:
        print ' [-] %s -  %s --> is down ' % (r.rstrip('\n'), ip)

def get_gateway(cidr):
    ip = IPNetwork(cidr)
    return ip[1]

def main():
    if len(sys.argv) <= 1:
        print "Use the -h option for help"
        exit(2)

    desc = "Network recognition tool"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-f', '--file', required=False, help='IP/domain list')
    parser.add_argument('-t', '--target', required=False, help='IP or Domain')
    args = parser.parse_args()
    filename = args.file
    ip_range = args.target

    if ip_range is not None:
        gateway = get_gateway(ip_range)
        ping_process(ip_range, gateway)
    elif filename is not None:
        for network in open(filename, 'r'):
            gateway = get_gateway(network)
            ping_process(network, gateway)

if __name__ == '__main__':
    main()

