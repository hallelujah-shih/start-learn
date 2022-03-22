from ipaddress import IPV4LENGTH
from socket import TCP_CORK
from typing import Protocol
from scapy.all import *


nl = IP(dst="127.0.0.1", ttl=64, id=0x1234, proto=6)
tl = TCP(sport=0x1234, dport=0x1234, flags="S", seq=0x4321, ack=0)

for i in range(20):
    send(nl/raw(tl)[:-6])
