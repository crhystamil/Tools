#!/usr/bin/env python
from netaddr import *
import pyping
import argparse, sys

def ping_process(r, ip_1, ip_2, mode):
    resp_1 = pyping.ping(str(ip_1))
    if resp_1.ret_code == 0:
        print_v(r, ip_1, "up")
    else:
        print_v(r, ip_1, "down", mode)
    if resp_1.ret_code != 0:
        resp_2 = pyping.ping(str(ip_2))
        if resp_2.ret_code == 0:
            print_v(r, ip_2, "up")
        else:
            print_v(r, ip_2, "down", mode)

def print_v(r, ip, status, mode=False):
    TGREEN =  '\033[32m'
    ENDC = '\033[m'
    if status == "up":
        print(TGREEN + " [*] %s -  %s --> is up " + ENDC) % (r.rstrip('\n'), ip)
    elif mode: 
        print(" [*] %s -  %s --> is down ") % (r.rstrip('\n'), ip)

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
    parser.add_argument('-V', '--verbose', required=False, help='Mode verbose')
    args = parser.parse_args()
    filename = args.file
    ip_range = args.target
    mode = args.verbose

    if ip_range is not None:
        gateway = get_gateway(ip_range)
        ping_process(ip_range, gateway[0], gateway[1], mode)
    elif filename is not None:
        for network in open(filename, 'r'):
            gateway = get_gateway(network)
            ping_process(network, gateway[0], gateway[1], mode)

if __name__ == '__main__':
    main()

