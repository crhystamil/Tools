#!/usr/bin/env python
from netaddr import *
import pyping
import argparse, sys

def ping_process(r, ip_1, ip_2):
    TGREEN =  '\033[32m'
    ENDC = '\033[m'
    resp_1 = pyping.ping(str(ip_1))
    resp_2 = pyping.ping(str(ip_2))
    if resp_1.ret_code == 0:
        print(TGREEN + " [*] %s -  %s --> is up " + ENDC) % (r.rstrip('\n'), ip_1)
    else:
        print ' [-] %s -  %s --> is down ' % (r.rstrip('\n'), ip_1)

    if resp_2.ret_code == 0:
        print(TGREEN + " [*] %s -  %s --> is up " + ENDC) % (r.rstrip('\n'), ip_2)
    else:
        print ' [-] %s -  %s --> is down ' % (r.rstrip('\n'), ip_2)

def get_gateway(cidr):
    ip = IPNetwork(cidr)
    res = [ip[1],ip[-2]]
    return res

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
            ping_process(network, gateway[0], gateway[1])

if __name__ == '__main__':
    main()

