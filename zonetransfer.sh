#!/bin/bash

if [ -z "$1" ]; then
    echo "[*] Simple Zone Transfer Script"
    echo "[*] Usage: $0 <domain name>"
    exit 0
fi

if [ -f $1 ]; then
    echo "[*] Read file"
    while read -r line; do
        echo "[*] Test zone transfer to domain: $line"
        for server in $(host -t ns $line| cut -d " " -f 4);do
            host -l $line $server |grep "has address"
        done
    done < "$1"
else
    echo "[*] Test zone transfer to domain: $1"
    for server in $(host -t ns $1| cut -d " " -f 4);do
        host -l $1 $server |grep "has address"
    done

fi
