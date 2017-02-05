import socket
import time
from scapy.all import *
from bgp import *

update = {}

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
	
	global update
	if pkt[IP].src == '3.3.3.3':
		if str(pkt.summary()).find("BGPHeader") > 0:
			if pkt[BGPHeader].type == 1:
				send(IP(dst=pkt[IP].src)/TCP(sport=pkt[TCP].dport,dport=pkt[TCP].sport,ack=pkt[TCP].seq+1,seq=pkt[TCP].ack,flags="PA")/BGPHeader(type=1)/BGPOpen(version=4,AS=65000,hold_time=180,bgp_id='7.7.7.7'))
				return "Open sent"
			elif pkt[BGPHeader].type == 2:
				send(IP(dst=pkt[IP].src)/TCP(sport=pkt[TCP].dport,dport=pkt[TCP].sport,ack=pkt[TCP].seq+1,seq=pkt[TCP].ack,flags="PA")/BGPHeader(type=4,len=19))
				return "Update reply sent"
			elif pkt[BGPHeader].type == 3:
				return "Notification Received"
			else:
				if update:
					update=eval(update)

					if update['TYPE'] == 0: #To match BGP update type
						send(IP(dst=pkt[IP].src)/TCP(sport=pkt[TCP].dport,dport=pkt[TCP].sport,ack=pkt[TCP].seq+1,seq=pkt[TCP].ack,flags="PA")/BGPHeader(type=4,len=19)/BGPHeader(type=2)/BGPUpdate(nlri=update['NLRI'], total_path=[BGPPathAttribute(type='ORIGIN', value=update['ORIGIN']),BGPPathAttribute(type='NEXT_HOP', value=update['NEXT_HOP']),BGPPathAttribute(flags=128L,type='MULTI_EXIT_DISC', value=update['MULTI_EXIT_DISC']),BGPPathAttribute(type='LOCAL_PREF', value=update['LOCAL_PREF']),BGPPathAttribute(type='AS_PATH', value=update['AS_PATH'])]))
						update = {}
						return "Update sent"

					else: #sending bgp withdraw + keepalive
						send(IP(dst=pkt[IP].src)/TCP(sport=pkt[TCP].dport,dport=pkt[TCP].sport,ack=pkt[TCP].seq+1,seq=pkt[TCP].ack,flags="PA")/BGPHeader(type=4,len=19)/BGPHeader(type=2)/BGPUpdate(withdrawn=update['NLRI']))
						update = {}
						return "Withdrawn sent"				
				else:
					#sending regular bgp keep_alive
					send(IP(dst=pkt[IP].src)/TCP(sport=pkt[TCP].dport,dport=pkt[TCP].sport,ack=pkt[TCP].seq+1,seq=pkt[TCP].ack,flags="PA")/BGPHeader(type=4,len=19))
					return "Keep_alive sent"

	else:
		#capturing self-looped packet with BGP Update
        	if pkt[IP].src=='127.0.0.1' and pkt[IP].src=='127.0.0.1':
			
			update=pkt[Raw].load
			return update

	


sniff(filter='tcp', stop_filter=stopfilter, store=0, prn=p_display)

#closing off the connection
conn.close()

'''
#############
BGP withdraw:
#############

update={'TYPE':1,'NLRI':[(mask,'prefix')],'PEER':'ip'}

##############
BGP PA update:
##############

update={'TYPE':0,'ORIGIN':'\x00','NEXT_HOP':'\xc0\xa8\x08\xc8','MULTI_EXIT_DISC':'\x00\x00\x00\x00','LOCAL_PREF':'\x00\x00\x00\x96','NLRI':[(32, '1.1.1.1')],'AS_PATH':'','PEER':'ip'}

##########
 Packet
##########

send(IP()/TCP()/Raw(load=update))


'''
