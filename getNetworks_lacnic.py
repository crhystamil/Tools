#!/usr/bin/env python3

import argparse, sys, socket, validators, requests, time
import urllib3

RDAP_IP='https://rdap.lacnic.net/rdap/ip/'
RDAP_ENTITY='https://rdap.lacnic.net/rdap/entity/'

def get_ip(domain):
    ip = ''
    try:
        ip = socket.gethostbyname(domain)
    except Exception as e:
        print("Error in domain: %s -> %s " %(domain,e))
#        pass
    if isValid_ip(ip):
        return ip 

def rdap_ip(ip):
    id_rdap = None
    try:
        data = requests.get(RDAP_IP+ip)
        rdap = data.json()
        if rdap.get('errorCode'):
            print('Query rate limite exceeded rdap_ip')
        else: 
            id_rdap = rdap['entities'][0]['handle']
    except Exception as e:
        print("Error in request rdap_ip: ", e)
        pass
    return id_rdap

def rdap_entity(name):
    name_rdap = ''
    try:
        data = requests.get(RDAP_ENTITY+name)
        rdap = data.json()
        if rdap.get('errorCode'):
            print(rdap['errorCode'],rdap['description'][0])
        else:
            print('name: ', rdap['vcardArray'][1][1][3])
            print('autnum: ', rdap['autnums'][0]['handle'])
            for a in rdap['networks']:
                print(a['handle'])

    except Exception as e:
#        print("error in radp entity:", e)
        pass

def isValid_ip(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:
        return False

    return True


def main():

    if len(sys.argv) <= 1:
        print('use the -h or --help option for help.')
        exit(2)

    desc = "search the ASN by IP"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-t', '--target',  help='IP or domain')
    parser.add_argument('-f', '--file', help='list of ip or domain')
    args = parser.parse_args()

    target = args.target
    target_file = args.file

    if target is not None:
        print(" Get data to: ", target)
        if isValid_ip(target):
            rdap_entity(rdap_ip(target))
        elif validators.domain(target):
            ip = get_ip(target)
            rdap_entity(rdap_ip(ip))
        print(" ----------------------------------------------------")
    elif target_file is not None:
        for dom_ip in open(target_file,'r').readlines():
            print("Get data to: ", dom_ip)
            if isValid_ip(dom_ip.rstrip('\n')):
                ip1 = rdap_ip(dom_ip)
                if ip1 is not None:
                    rdap_entity(ip1)
            elif validators.domain(dom_ip.rstrip('\n')):
                ip2 = get_ip(dom_ip.rstrip('\n'))
                if ip2 is not None:
                    ip3 = rdap_ip(ip2)
                    if ip3 is not None:
                        rdap_entity(ip3)
            print(" ----------------------------------------------------")
            time.sleep(15)


if __name__ == '__main__':
    banner = "baner IP"
#    print(banner)
    main()
