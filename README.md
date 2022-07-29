# NetworkAnalyzer

> Send or capture any packet (sequence of bytes) on any interface desired.

## Table of Contents

- [NetworkAnalyzer](#networkanalyzer)
  - [Table of Contents](#table-of-contents)
  - [Send raw packets](#send-raw-packets)
    - [Example](#example)
  - [Send TCP SYN packet](#send-tcp-syn-packet)
    - [Example](#example-1)
  - [Capture TCP SYN-ACK packets](#capture-tcp-syn-ack-packets)
    - [Example](#example-2)
  - [Scan open ports of a target](#scan-open-ports-of-a-target)
    - [Example](#example-3)

## Send raw packets

By using `pkt_sender.py` you can send any sequence of bytes through the chosen interface. If your interface uses `ethernet` protocol as the link layer protocol (it probably does), the packet should be at least 14 bytes.

If you want the packet to be a valid ethernet packet you must follow the ethernet frame format shown below.

| # | Destination MAC Address | Source MAC Address | EtherType | Payload
| :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| **Size** | 6 bytes | 6 bytes | 2 bytes | Up to 1500 bytes
| **Sample Format** | _F3054290A2C6_ | _5E0781A2BB0D_ | _0080_ |

Using 80 as EthernetType means you want to use IP as the network layer.

You can list your interfaces with the command below:

```bash
$ ip link

1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: wlp3s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DORMANT group default qlen 1000
    link/ether 00:00:00:00:00:00 brd ff:ff:ff:ff:ff:ff
```

### Example

Sending an packet without payload through the _wlp3s0_ interface:

```bash
$ sudo python3 pkt_sender.py

Content of your packet: F3054290A2C65E0781A2BB0D0080
Interface: wlp3s0
Sent 14-byte packet on wlp3s0
```

## Send TCP SYN packet

You can use `tcp_syn_sender.py` to send TCP SYN packets. You should specify packet's information in `info.txt` like this:

```text
Dest IP:                 93.184.216.34
Dest Port:               80
Src IP:                  192.168.200.221
Src Port:                3000
Interface:               wlp3s0
Interface's Mac Address: 70:66:55:c0:9f:53 
Gateway's Mac Address:   96:8d:38:93:ec:8b
```

You can run `info.sh` bash script to create this file for you.

```bash
$ chmod +x info.sh

# ./info.sh DestIP DestPort Interface SrcPort
$ ./info.sh 93.184.216.34 80 wlp3s0 3000
```

### Example

By running `tcp_syn_sender.py` your packet will be sent

```bash
$ sudo python3 tcp_syn_sender.py

TCP SYN packet sent to 93.184.216.34:80 through wlp3s0
```

## Capture TCP SYN-ACK packets

Wireshark is a packet sniffer and analysis tool. It captures network traffic on the local network and stores the data for analysis.

our _miniwireshark_ is a special-purpose Wireshark, which captures all TCP SYN-ACK packets, our host is receiving.

### Example

```bash
$ sudo python3 miniwireshark.py

Port 443 is open on 50.16.232.21
Port 80 is open on 93.184.216.34
```

## Scan open ports of a target

Nmap is a network scanner to discover hosts and services on a computer network by sending packets and analyzing the responses.

`mininmap.py` and `mininmap_tcp_socket.py` are written to send TCP SYN packets to a range of ports of a target machine. `mininmap.py` sends TCP packets using raw socket, but `mininmap_tcp_socket.py` uses python's TCP socket and it's multi-threaded.

You can use _mininmap_ combined with _miniwireshark_ to scan target ports.

### Example

![nmap_wireshark](https://user-images.githubusercontent.com/74505991/181753209-760f34c5-d2d2-4dd6-a241-ee8b375933a9.png)
