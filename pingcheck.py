import sys
from scapy.all import *
print("pinging the target....")
ip = "13.233.75.187"   # command line argument
icmp = IP(dst=ip)/ICMP()
#IP defines the protocol for IP addresses
#dst is the destination IP address
#TCP defines the protocol for the ports
resp = sr1(icmp,timeout=5)
if resp == None:
    print("This host is down")
else:
    print("This host is up")