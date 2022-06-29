echo $1 > info.txt
echo $2 >> info.txt
ifconfig $3 | awk '/inet / {print $2}' >> info.txt
echo $4 >> info.txt
echo $3 >> info.txt
ip -o link | grep $3 | grep -oP "link\/ether \K\w+(.*?) " | sed 's/:/ /g' >> info.txt
arp -n | sed -n 2p | awk '{print $3}' | sed 's/:/ /g' >> info.txt
echo 'bash info.sh 93.184.216.34 80 wlp3s0 3000' >> info.txt