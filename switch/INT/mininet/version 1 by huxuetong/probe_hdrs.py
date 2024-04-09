from scapy.all import *

TYPE_PROBE = 0x812

class Probe(Packet):
   fields_desc = [ ByteField("hop_cnt", 0),
                   ByteField("data_cnt", 0)]

class ProbeData(Packet):
   fields_desc = [ ByteField("swid", 0),
                   ByteField("port", 0),
                   IntField("byte_cnt", 0),
                   IntField("pckcont", 0),
                   IntField("enpckcont", 0),
                   BitField("last_time", 0, 48),
                   BitField("cur_time", 0, 48),
                   BitField("in_time", 0, 48),
                   BitField("qdepth", 0, 32)]

class ProbeFwd(Packet):
   fields_desc = [ ByteField("egress_spec", 0)]

bind_layers(Ether, Probe, type=TYPE_PROBE)
bind_layers(Probe, ProbeFwd, data_cnt=0)
bind_layers(Probe, ProbeData)
bind_layers(ProbeData, ProbeData)
bind_layers(ProbeData, ProbeFwd)
bind_layers(ProbeFwd, ProbeFwd)







