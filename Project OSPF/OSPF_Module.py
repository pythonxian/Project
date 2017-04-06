#!/usr/bin/env python

# scapy.contrib.description = OSPF
# scapy.contrib.status = loads

from scapy.all import *
from scapy.layers.inet import IP
#from inet6 import *

EXT_VERSION = "v0.9.2"


class OSPFOptionsField(FlagsField):

    def __init__(self, name="options", default=0, size=8,
                 names=["MT", "E", "MC", "NP", "L", "DC", "O", "DN"]):
        FlagsField.__init__(self, name, default, size, names)


_OSPF_types = {1: "Hello",
               2: "DBDesc",
               3: "LSReq",
               4: "LSUpd",
               5: "LSAck"}


class OSPF_Hdr(Packet):
    name = "OSPF Header"
    fields_desc = [
                    ByteField("version", 2),
                    ByteEnumField("type", 1, _OSPF_types),
                    ShortField("len", None),
                    IPField("src", "1.1.1.1"),
                    IPField("area", "0.0.0.0"), # default: backbone
                    XShortField("chksum", None),
                    ShortEnumField("authtype", 0, {0:"Null", 1:"Simple", 2:"Crypto"}),
                    # Null or Simple Authentication
                    ConditionalField(XLongField("authdata", 0), lambda pkt:pkt.authtype != 2),
                    # Crypto Authentication
                    ConditionalField(XShortField("reserved", 0), lambda pkt:pkt.authtype == 2),
                    ConditionalField(ByteField("keyid", 1), lambda pkt:pkt.authtype == 2),
                    ConditionalField(ByteField("authdatalen", 0), lambda pkt:pkt.authtype == 2),
                    ConditionalField(XIntField("seq", 0), lambda pkt:pkt.authtype == 2),
                    # TODO: Support authdata (which is appended to the packets as if it were padding)
                    ]

    def post_build(self, p, pay):
        # TODO: Remove LLS data from pay
        # LLS data blocks may be attached to OSPF Hello and DD packets
        # The length of the LLS block shall not be included into the length of OSPF packet
        # See <http://tools.ietf.org/html/rfc5613>
        p += pay
        l = self.len
        if l is None:
            l = len(p)
            p = p[:2] + struct.pack("!H", l) + p[4:]
        if self.chksum is None:
            if self.authtype == 2:
                ck = 0   # Crypto, see RFC 2328, D.4.3
            else:
                # Checksum is calculated without authentication data
                # Algorithm is the same as in IP()
                ck = checksum(p[:16] + p[24:])
                p = p[:12] + chr(ck >> 8) + chr(ck & 0xff) + p[14:]
            # TODO: Handle Crypto: Add message digest  (RFC 2328, D.4.3)
        return p

    def hashret(self):
        return struct.pack("H", self.area) + self.payload.hashret()

    def answers(self, other):
        if (isinstance(other, OSPF_Hdr) and
            self.area == other.area and
            self.type == 5):  # Only acknowledgements answer other packets
                return self.payload.answers(other.payload)
        return 0


class OSPF_Hello(Packet):
    name = "OSPF Hello"
    fields_desc = [IPField("mask", "255.255.255.0"),
                   ShortField("hellointerval", 10),
                   OSPFOptionsField(),
                   ByteField("prio", 1),
                   IntField("deadinterval", 40),
                   IPField("router", "0.0.0.0"),
                   IPField("backup", "0.0.0.0"),
                   FieldListField("neighbors", [], IPField("", "0.0.0.0"), length_from=lambda pkt: (pkt.underlayer.len - 44))]

    def guess_payload_class(self, payload):
        # check presence of LLS data block flag
        if self.options & 0x10 == 0x10:
            return OSPF_LLS_Hdr
        else:
            return Packet.guess_payload_class(self, payload)


class LLS_Generic_TLV(Packet):
    name = "LLS Generic"
    fields_desc = [ShortField("type", 1),
                   FieldLenField("len", None, length_of=lambda x: x.val),
                   StrLenField("val", "", length_from=lambda x: x.len)]

    def guess_payload_class(self, p):
        return Padding


class LLS_ExtendedOptionsField(FlagsField):

    def __init__(self, name="options", default=0, size=32,
                 names=["LR", "RS"]):
        FlagsField.__init__(self, name, default, size, names)


class LLS_Extended_Options(LLS_Generic_TLV):
    name = "LLS Extended Options and Flags"
    fields_desc = [ShortField("type", 1),
                   ShortField("len", 4),
                   LLS_ExtendedOptionsField()]


class LLS_Crypto_Auth(LLS_Generic_TLV):
    name = "LLS Cryptographic Authentication"
    fields_desc = [ShortField("type", 2),
                   FieldLenField("len", 20, fmt="B", length_of=lambda x: x.authdata),
                   XIntField("sequence", "\x00\x00\x00\x00"),
                   StrLenField("authdata", "\x00" * 16, length_from=lambda x: x.len)]

    def post_build(self, p, pay):
        p += pay
        l = self.len

        if l is None:
            # length = len(sequence) + len(authdata) + len(payload)
            l = len(p[3:])
            p = p[:2] + struct.pack("!H", l) + p[3:]

        return p

_OSPF_LLSclasses = {1: "LLS_Extended_Options",
                    2: "LLS_Crypto_Auth"}


def _LLSGuessPayloadClass(p, **kargs):
    """ Guess the correct LLS class for a given payload """

    cls = Raw
    if len(p) >= 4:
        typ = struct.unpack("!H", p[0:2])[0]
        clsname = _OSPF_LLSclasses.get(typ, "LLS_Generic_TLV")
        cls = globals()[clsname]
    return cls(p, **kargs)


class OSPF_LLS_Hdr(Packet):
    name = "OSPF Link-local signaling"
    fields_desc = [XShortField("chksum", None),
                   # FIXME Length should be displayed in 32-bit words
                   ShortField("len", None),
                   PacketListField("llstlv", [], _LLSGuessPayloadClass)]

    def post_build(self, p, pay):
        p += pay
        l = self.len
        if l is None:
            # Length in 32-bit words
            l = len(p) / 4
            p = p[:2] + struct.pack("!H", l) + p[4:]
        if self.chksum is None:
            c = checksum(p)
            p = chr((c >> 8) & 0xff) + chr(c & 0xff) + p[2:]
        return p

_OSPF_LStypes = {1: "router",
                 2: "network",
                 3: "summaryIP",
                 4: "summaryASBR",
                 5: "external",
                 7: "NSSAexternal"}

_OSPF_LSclasses = {1: "OSPF_Router_LSA",
                   2: "OSPF_Network_LSA",
                   3: "OSPF_SummaryIP_LSA",
                   4: "OSPF_SummaryASBR_LSA",
                   5: "OSPF_External_LSA",
                   7: "OSPF_NSSA_External_LSA"}


def ospf_lsa_checksum(lsa):
    """ Fletcher checksum for OSPF LSAs, returned as a 2 byte string.
    Give the whole LSA packet as argument.
    For details on the algorithm, see RFC 2328 chapter 12.1.7 and RFC 905 Annex B.
    """
    # This is based on the GPLed C implementation in Zebra <http://www.zebra.org/>

    CHKSUM_OFFSET = 16

    if len(lsa) < CHKSUM_OFFSET:
        raise Exception("LSA Packet too short (%s bytes)" % len(lsa))

    c0 = c1 = 0
    # Calculation is done with checksum set to zero
    lsa = lsa[:CHKSUM_OFFSET] + "\x00\x00" + lsa[CHKSUM_OFFSET + 2:]
    for char in lsa[2:]:  #  leave out age
        c0 += ord(char)
        c1 += c0

    c0 %= 255
    c1 %= 255

    x = ((len(lsa) - CHKSUM_OFFSET - 1) * c0 - c1) % 255

    if (x <= 0):
        x += 255

    y = 510 - c0 - x

    if (y > 255):
        y -= 255
    #checksum = (x << 8) + y

    return chr(x) + chr(y)


class OSPF_LSA_Hdr(Packet):
    name = "OSPF LSA Header"
    fields_desc = [ShortField("age", 1),
                   OSPFOptionsField(),
                   ByteEnumField("type", 1, _OSPF_LStypes),
                   IPField("id", "192.168.0.0"),
                   IPField("adrouter", "1.1.1.1"),
                   XIntField("seq", 0x80000001),
                   XShortField("chksum", 0),
                   ShortField("len", 36)]

    def extract_padding(self, s):
        return "", s


_OSPF_Router_LSA_types = {1: "p2p",
                          2: "transit",
                          3: "stub",
                          4: "virtual"}


class OSPF_Link(Packet):
    name = "OSPF Link"
    fields_desc = [IPField("id", "192.168.0.0"),
                   IPField("data", "255.255.255.0"),
                   ByteEnumField("type", 3, _OSPF_Router_LSA_types),
                   ByteField("toscount", 0),
                   ShortField("metric", 10),
                   # TODO: define correct conditions
                   ConditionalField(ByteField("tos", 0), lambda pkt: False),
                   ConditionalField(ByteField("reserved", 0), lambda pkt: False),
                   ConditionalField(ShortField("tosmetric", 0), lambda pkt: False)]

    def extract_padding(self, s):
        return "", s


def _LSAGuessPayloadClass(p, **kargs):
    """ Guess the correct LSA class for a given payload """
    # This is heavily based on scapy-cdp.py by Nicolas Bareil and Arnaud Ebalard
    # XXX: This only works if all payload
    cls = Raw
    if len(p) >= 4:
        typ = struct.unpack("!B", p[3])[0]
        clsname = _OSPF_LSclasses.get(typ, "Raw")
        cls = globals()[clsname]
    return cls(p, **kargs)


class OSPF_BaseLSA(Packet):
    """ An abstract base class for Link State Advertisements """

    def post_build(self, p, pay):
        length = self.len
        if length is None:
            length = len(p)
            p = p[:18] + struct.pack("!H", length) + p[20:]
        if self.chksum is None:
            chksum = ospf_lsa_checksum(p)
            p = p[:16] + chksum + p[18:]
        return p    # p+pay?

    def extract_padding(self, s):
        length = self.len
        return "", s


class OSPF_Router_LSA(OSPF_BaseLSA):
    name = "OSPF Router LSA"
    fields_desc = [ShortField("age", 1),
                   OSPFOptionsField(),
                   ByteField("type", 1),
                   IPField("id", "1.1.1.1"),
                   IPField("adrouter", "1.1.1.1"),
                   XIntField("seq", 0x80000001),
                   XShortField("chksum", None),
                   ShortField("len", None),
                   FlagsField("flags", 0, 8, ["B", "E", "V", "W", "Nt"]),
                   ByteField("reserved", 0),
                   FieldLenField("linkcount", None, count_of="linklist"),
                   PacketListField("linklist", [], OSPF_Link, count_from=lambda pkt: pkt.linkcount, length_from=lambda pkt: pkt.linkcount * 12)]


class OSPF_Network_LSA(OSPF_BaseLSA):
    name = "OSPF Network LSA"
    fields_desc = [ShortField("age", 1),
                   OSPFOptionsField(),
                   ByteField("type", 2),
                   IPField("id", "192.168.0.0"),
                   IPField("adrouter", "1.1.1.1"),
                   XIntField("seq", 0x80000001),
                   XShortField("chksum", None),
                   ShortField("len", None),
                   IPField("mask", "255.255.255.0"),
                   FieldListField("routerlist", [], IPField("", "1.1.1.1"), length_from=lambda pkt: pkt.len - 24)]


class OSPF_SummaryIP_LSA(OSPF_BaseLSA):
    name = "OSPF Summary LSA (IP Network)"
    fields_desc = [ShortField("age", 1),
                   OSPFOptionsField(),
                   ByteField("type", 3),
                   IPField("id", "192.168.0.0"),
                   IPField("adrouter", "1.1.1.1"),
                   XIntField("seq", 0x80000001),
                   XShortField("chksum", None),
                   ShortField("len", None),
                   IPField("mask", "255.255.255.0"),
                   ByteField("reserved", 0),
                   X3BytesField("metric", 10),
                   # TODO: Define correct conditions
                   ConditionalField(ByteField("tos", 0), lambda pkt:False),
                   ConditionalField(X3BytesField("tosmetric", 0), lambda pkt:False)]


class OSPF_SummaryASBR_LSA(OSPF_SummaryIP_LSA):
    name = "OSPF Summary LSA (AS Boundary Router)"
    type = 4
    id = "2.2.2.2"
    mask = "0.0.0.0"
    metric = 20


class OSPF_External_LSA(OSPF_BaseLSA):
    name = "OSPF External LSA (ASBR)"
    fields_desc = [ShortField("age", 1),
                   OSPFOptionsField(),
                   ByteField("type", 5),
                   IPField("id", "192.168.0.0"),
                   IPField("adrouter", "2.2.2.2"),
                   XIntField("seq", 0x80000001),
                   XShortField("chksum", None),
                   ShortField("len", None),
                   IPField("mask", "255.255.255.0"),
                   FlagsField("ebit", 0, 1, ["E"]),
                   BitField("reserved", 0, 7),
                   X3BytesField("metric", 20),
                   IPField("fwdaddr", "0.0.0.0"),
                   XIntField("tag", 0),
                   # TODO: Define correct conditions
                   ConditionalField(ByteField("tos", 0), lambda pkt:False),
                   ConditionalField(X3BytesField("tosmetric", 0), lambda pkt:False)]


class OSPF_NSSA_External_LSA(OSPF_External_LSA):
    name = "OSPF NSSA External LSA"
    type = 7


class OSPF_DBDesc(Packet):
    name = "OSPF Database Description"
    fields_desc = [ShortField("mtu", 1500),
                   OSPFOptionsField(),
                   FlagsField("dbdescr", 0, 8, ["MS", "M", "I", "R", "4", "3", "2", "1"]),
                   IntField("ddseq", 1),
                   PacketListField("lsaheaders", None, OSPF_LSA_Hdr,
                                    count_from = lambda pkt: None,
                                    length_from = lambda pkt: pkt.underlayer.len - 24 - 8)]

    def guess_payload_class(self, payload):
        # check presence of LLS data block flag
        if self.options & 0x10 == 0x10:
            return OSPF_LLS_Hdr
        else:
            return Packet.guess_payload_class(self, payload)


class OSPF_LSReq_Item(Packet):
    name = "OSPF Link State Request (item)"
    fields_desc = [IntEnumField("type", 1, _OSPF_LStypes),
                   IPField("id", "1.1.1.1"),
                   IPField("adrouter", "1.1.1.1")]

    def extract_padding(self, s):
        return "", s


class OSPF_LSReq(Packet):
    name = "OSPF Link State Request (container)"
    fields_desc = [PacketListField("requests", None, OSPF_LSReq_Item, count_from = lambda pkt:None, length_from = lambda pkt:pkt.underlayer.len - 24)]


class OSPF_LSUpd(Packet):
    name = "OSPF Link State Update"
    fields_desc = [FieldLenField("lsacount", None, fmt="!I", count_of="lsalist"),
                   PacketListField("lsalist", [], _LSAGuessPayloadClass, count_from = lambda pkt: pkt.lsacount, length_from = lambda pkt: pkt.underlayer.len - 24)]


class OSPF_LSAck(Packet):
    name = "OSPF Link State Acknowledgement"
    fields_desc = [PacketListField("lsaheaders", None, OSPF_LSA_Hdr,
                                   count_from = lambda pkt: None,
                                   length_from = lambda pkt: pkt.underlayer.len - 24)]

    def answers(self, other):
        if isinstance(other, OSPF_LSUpd):
            for reqLSA in other.lsalist:
                for ackLSA in self.lsaheaders:
                    if (reqLSA.type == ackLSA.type and
                        reqLSA.seq == ackLSA.seq):
                        return 1
        return 0




bind_layers(IP, OSPF_Hdr, proto=89)
bind_layers(OSPF_Hdr, OSPF_Hello, type=1)
bind_layers(OSPF_Hdr, OSPF_DBDesc, type=2)
bind_layers(OSPF_Hdr, OSPF_LSReq, type=3)
bind_layers(OSPF_Hdr, OSPF_LSUpd, type=4)
bind_layers(OSPF_Hdr, OSPF_LSAck, type=5)


