import socket
import time
from scapy.all import *
from bgp import *

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('192.168.8.107', 179))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr


def stopfilter(x):
    if x[TCP].flags == 25 and x[IP].src == '3.3.3.3':
        
        return True
    else:
        return False


def p_display(pkt):
    if pkt[IP].src == '3.3.3.3':
        if str(pkt.summary()).find("BGPHeader") > 0:
            if pkt[BGPHeader].type == 1:
                send(IP(dst=pkt[IP].src)/TCP(sport=pkt[TCP].dport, dport=pkt[TCP].sport, ack=pkt[TCP].seq + 1,seq=pkt[TCP].ack, flags="PA")/BGPHeader(type=1)/BGPOpen(version=4,AS=65000,hold_time=180,bgp_id='7.7.7.7'))
                return "Open Message sent"
            elif pkt[BGPHeader].type == 2:
                send(IP(dst=pkt[IP].src)/TCP(sport=pkt[TCP].dport, dport=pkt[TCP].sport, ack=pkt[TCP].seq + 1,seq=pkt[TCP].ack, flags="PA") / BGPHeader(type=4, len=19))
                return "Update reply sent"
            elif pkt[BGPHeader].type == 3:
                return "Notification Received"
            else:
                # sending regular bgp keep_alive
                send(IP(dst=pkt[IP].src) / TCP(sport=pkt[TCP].dport, dport=pkt[TCP].sport, ack=pkt[TCP].seq + 1,seq=pkt[TCP].ack, flags="PA") / BGPHeader(type=4, len=19))
                return "Keep_alive sent"



sniff(filter='tcp', stop_filter=stopfilter, store=0, prn=p_display)

#closing off the connection
conn.close()
