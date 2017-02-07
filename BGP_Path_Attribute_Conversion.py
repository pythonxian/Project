import sys

#AS Path Attributes
pst= raw_input("Please Enter AS PATH TYPE, 1 FOR AS_SET, 2 FOR AS_SEQ :")
psv = raw_input("Please Enter the AS number, eg(65100, 65000): ")
psl=len(psv.split(","))

#Local Preference Attribute
loc = raw_input("Please Enter the Local Perference value :")

#MED Metric Attribute
med = raw_input("Please Enter the MED Metric value :")

#Next Hop
next_hop = raw_input("Please Enter the Next Hop IP address :")
next_hop = next_hop.split('.')

as_path = [chr(int(pst)),chr(int(psl))]


def binsplit(s):
	
	o = []
	while s:
    		o.append(s[:8])
    		s = s[8:]
	return o 


#Convert ASCII AS number into character

def AS_convert(psv, as_path):
	for i in psv.split(","):
		for ii in binsplit(bin(int(i))[2:].zfill(16)):
			as_path.append(chr(int(ii,2)))
	return as_path	

#Convert ASCII MED OR LOC number into character

def LOC_MED_convert(num):
	med_loc=[]
	for i in binsplit(bin(int(mum))[2:].zfill(32)):
		med_loc.append(chr(int(i,2)))
	return med_loc


#Convert ASCII NEXT_HOP number into character


def Next_Hop_convert(next_hop):
	for i in range(len(next_hop)):
		next_hop[i] = chr(int(next_hop[i]))
	return next_hop




print "The converted AS Path attribute value is:\n %s" %AS_convert(psv,as_path)
print "The converted Local Preference value is:\n %s" %LOC_MED_convert(loc)
print "The converted MED Metric value is:\n %s" %LOC_MED_convert(med)
print "The converted Next Hop IP is:\n %s" %Next_Hop_convert(next_hop)


