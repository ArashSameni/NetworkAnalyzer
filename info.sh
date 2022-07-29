#!/bin/bash

if [[ $# -eq 4 ]]
then
    src_ip=$(ifconfig $3 | awk '/inet / {print $2}')
    interface_mac_addr=$(ip -o link | grep $3 | grep -oP "link\/ether \K\w+(.*?) ")
    gateway_mac_addr=$(arp -n | sed -n 2p | awk '{print $3}')

    echo "Dest IP:                 ${1}" > info.txt
    echo "Dest Port:               ${2}" >> info.txt
    echo "Src IP:                  ${src_ip}" >> info.txt
    echo "Src Port:                ${4}" >> info.txt
    echo "Interface:               ${3}" >> info.txt
    echo "Interface's Mac Address: ${interface_mac_addr}" >> info.txt
    echo "Gateway's Mac Address:   ${gateway_mac_addr}" >> info.txt
else
    echo "Not enough arguments"
    echo "Usage: ./info.sh DestIP DestPort Interface SrcPort"
fi