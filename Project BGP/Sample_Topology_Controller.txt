import socket
import time
from scapy.all import *
from bgp import *
next_hop=""

update={'TYPE':0,'ORIGIN':'\x00','NEXT_HOP':next_hop,'MULTI_EXIT_DISC':'\x00\x00\x00\x00','LOCAL_PREF':'\x00\x00\x00d','NLRI':[(32, '22.22.22.2')],'AS_PATH':'','COMMUNITY':'\xff\xff\xff\x02'}
withdraw={'TYPE':1,'NLRI':[(32, '22.22.22.2')]}

sr={"South":("172.16.22.2",443), "North":("172.16.13.1",443)}

 
def is_alive(ss):

 
    # Create a socket object to connect with
    s = socket.socket()
    
    # Now try connecting, passing in a tuple with address & port
    try:
        s.connect(ss)
        return True
    except socket.error:
        return False
    finally:
        s.close()


while True:
	if is_alive(sr['North']):
		if not next_hop:
			next_hop = '\x01\x01\x01\x01'
			update['NEXT_HOP'] = next_hop
			print update
			send(IP()/TCP()/Raw(load=update))
		elif next_hop == '\x02\x02\x02\x02':
			next_hop = '\x01\x01\x01\x01'
			update['NEXT_HOP'] = next_hop
			print update
			send(IP()/TCP()/Raw(load=update))
		else:
			continue
	elif is_alive(sr['South']):
		if not next_hop:
			next_hop = '\x02\x02\x02\x02'
			update['NEXT_HOP'] = next_hop
			print update
			send(IP()/TCP()/Raw(load=update))
		elif next_hop == '\x01\x01\x01\x01':
			next_hop ='\x02\x02\x02\x02'
			update['NEXT_HOP'] = next_hop
			print update
			send(IP()/TCP()/Raw(load=update))
		else:
			continue
	else:
		if not next_hop:
			print "Both sides are down"
			continue
		else:
			
			send(IP()/TCP()/Raw(load=withdraw))
			next_hop=""
	
	time.sleep(10)




