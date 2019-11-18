#!/usr/bin/bash

if [ -d "./list_network" ]; then
    echo " [*] ---------------------------------"
else
    mkdir list_network
    echo " [*] create directory"
    echo " [*] ---------------------------------"
fi

for ip_range in `cat range_ips.txt`;do
    echo "[**] generate IPs $ip_range"
    filename=`echo $ip_range | awk -F "/" {'print $1"_"$2".lst"'}`
    ./generate_ips.py $ip_range > list_network/$filename
done
