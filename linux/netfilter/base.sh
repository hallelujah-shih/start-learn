#!/bin/bash
iptables -F 2>&1

iptables -A INPUT -p all -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p tcp --syn -m state --state NEW -m multiport --dports 22,80,443 -j ACCEPT
