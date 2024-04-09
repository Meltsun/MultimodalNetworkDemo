/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>
//------------------------------------------------------------
// 定义协议号
const bit<16> TYPE_ARP = 0x0806;
const bit<16> TYPE_IPV4 = 0x0800;
const bit<8>  IP_PROTO_ICMP = 0x01;
const bit<8>  IP_PROTO_TCP = 0x06;
const bit<8>  IP_PROTO_UDP = 0x11;

register< bit<32> >(8) transmition_model;
//共8个寄存器，索引为32位，每个寄存器存一个32位的数
//transmition_model[0]=1，则使用ECCN，=0则不用
//transmition_model[1]=1，则使用多路径，=0则不用
register< bit<32> >(8) multipath_ability;
//共8个寄存器，索引为32位，每个寄存器存一个32位的数
//multipath_ability[0]=1，则支持多路径，=0则不支持
register< bit<32> >(8) multipath_count; 
//共8个寄存器，索引为32位，每个寄存器存32位的数
//multipath_count[2,3,4]分别代表端口2,3,4的发包量
register< bit<32> >(8) multipath_initial;
//共8个寄存器，索引为32位，每个寄存器存32位的数
//multipath_initial[2,3,4]分别代表端口2,3,4的发包初始量
register< bit<32> >(8) multipath_order;
//共8个寄存器，索引为32位，每个寄存器存32位的数
//multipath_order[2,3,4]分别代表端口2,3,4的发包顺序
//------------------------------------------------------------
// 定义首部
// 物理层首部
header ethernet_h {
    bit<48>  dst_mac;
    bit<48>  src_mac;
    bit<16>  ether_type;
}
//--------------------------
// ARP首部
header arp_h {
    bit<16>  hardware_type;
    bit<16>  protocol_type;
    bit<8>   HLEN;
    bit<8>   PLEN;
    bit<16>  OPER;
    bit<48>  sender_ha;
    bit<32>  sender_ip;
    bit<48>  target_ha;
    bit<32>  target_ip;
}
//--------------------------
// IPv4首部
header ipv4_h {
    bit<4>   version;
    bit<4>   ihl;
    bit<8>   diffserv;
    bit<16>  total_len;
    bit<16>  identification;
    bit<3>   flags;
    bit<13>  frag_offset;
    bit<8>   ttl;
    bit<8>   protocol;
    bit<16>  hdr_checksum;
    bit<32>  src_addr;
    bit<32>  dst_addr;
}
//--------------------------
// ICMP首部
header icmp_h {
    bit<8>   type;
    bit<8>   code;
    bit<16>  hdr_checksum;
}
//--------------------------
//TCP首部
header tcp_h {
    bit<16>  src_port;
    bit<16>  dst_port;
    bit<32>  seq_no;
    bit<32>  ack_no;
    bit<4>   data_offset;
    bit<4>   res;
    bit<8>   flags;
    bit<16>  window;
    bit<16>  checksum;
    bit<16>  urgent_ptr;
}
//--------------------------
//UDP首部
header udp_h {
    bit<16>  src_port;
    bit<16>  dst_port;
    bit<16>  hdr_length;
    bit<16>  checksum;
}
//--------------------------
struct metadata {
    bit<8> packet_can_multipath;
    bit<8> multipath_port;
}
//--------------------------
//完整首部
struct headers {
    ethernet_h               ethernet;
    arp_h                    arp;
    ipv4_h                   ipv4;
    icmp_h                   icmp;
    tcp_h                    tcp;
    udp_h                    udp;
}
//------------------------------------------------------------
parser c_parser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start {
        meta = {0, 0};
        transition parse_ethernet;
    }
    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.ether_type) {
            TYPE_ARP: parse_arp;
            TYPE_IPV4: parse_ipv4;
            default: accept;
        }
    }
    state parse_arp {
        packet.extract(hdr.arp);
        transition accept;
    }
    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol) {
            IP_PROTO_ICMP: parse_icmp;
            IP_PROTO_TCP: parse_tcp;
            IP_PROTO_UDP: parse_udp;
            default: accept;
        }
    }
    state parse_icmp {
        packet.extract(hdr.icmp);
        transition accept;
    }
    state parse_tcp {
       packet.extract(hdr.tcp);
       transition accept;
    }
    state parse_udp {
       packet.extract(hdr.udp);
       transition accept;
    }
}
//------------------------------------------------------------
control c_verify_checksum(inout headers hdr, 
                          inout metadata meta) {
    apply {

    }
}
//------------------------------------------------------------
control c_ingress(inout headers hdr, 
                  inout metadata meta, 
                  inout standard_metadata_t standard_metadata) {
    action _drop() {
        mark_to_drop(standard_metadata);
    }
    action packet_can_multipath() {
        meta.packet_can_multipath = 1;
    }
    action packet_cannot_multipath() {
        meta.packet_can_multipath = 0;
    }
    table ipv4_is_for_video {
        key = {
            hdr.ipv4.dst_addr: lpm;
        }
        actions = {
            packet_can_multipath;
            packet_cannot_multipath;
            _drop;
        }
        size = 1024;
        default_action = _drop();
    }
    action ipv4_multipath(bit<48> src_mac, bit<48> dst_mac, bit<9> port) {
        hdr.ethernet.src_mac = src_mac;
        hdr.ethernet.dst_mac = dst_mac;
        standard_metadata.egress_spec = port;
    }
    table ipv4_multipath_lpm {
        key = {
            meta.multipath_port: exact;
        }
        actions = {
            ipv4_multipath;
            _drop;
        }
        size = 1024;
        default_action = _drop();
    }
    action ipv4_singlepath(bit<48> src_mac, bit<48> dst_mac, bit<9> port) {
        hdr.ethernet.src_mac = src_mac;
        hdr.ethernet.dst_mac = dst_mac;
        standard_metadata.egress_spec = port;
    }
    table ipv4_singlepath_lpm {
        key = {
            hdr.ipv4.dst_addr: lpm;
        }
        actions = {
            ipv4_singlepath;
            _drop;
        }
        size = 1024;
        default_action = _drop();
    }
    apply {
        if (hdr.arp.isValid()) {
            // is the packet for arp
            if (hdr.arp.target_ip == 0x0aaaaa01) {
                //ask who is 10.170.170.1
                hdr.ethernet.dst_mac = hdr.ethernet.src_mac;
                hdr.ethernet.src_mac = 0x00000aaaaa01;
                hdr.arp.OPER = 2;
                hdr.arp.target_ha = hdr.arp.sender_ha;
                hdr.arp.target_ip = hdr.arp.sender_ip;
                hdr.arp.sender_ip = 0x0aaaaa01;
                hdr.arp.sender_ha = 0x00000aaaaa01;
                standard_metadata.egress_spec = standard_metadata.ingress_port;
            }
            else if (hdr.arp.target_ip == 0x0ab4b401) {
                //ask who is 10.180.180.1
                hdr.ethernet.dst_mac = hdr.ethernet.src_mac;
                hdr.ethernet.src_mac = 0x00000ab4b401;
                hdr.arp.OPER = 2;
                hdr.arp.target_ha = hdr.arp.sender_ha;
                hdr.arp.target_ip = hdr.arp.sender_ip;
                hdr.arp.sender_ip = 0x0ab4b401;
                hdr.arp.sender_ha = 0x00000ab4b401;
                standard_metadata.egress_spec = standard_metadata.ingress_port;
            }
        }
        //else if (hdr.probe.isValid()) {
            // is the packet for int
        //}
        else if (ipv4_is_for_video.apply().hit) {
            // is the packet for video
            bit<32> temp_eccn = 0;
            bit<32> temp_multipath = 0;
            transmition_model.read(temp_eccn, (bit<32>)0);
            transmition_model.read(temp_multipath, (bit<32>)1);
            if (temp_multipath == 1 && (hdr.tcp.isValid() || hdr.icmp.isValid())) {
                // the tcp packet should be forwarded multipath
                //dadadadadaad
                bit<32> temp_multipath_ability = 0;
                multipath_ability.read(temp_multipath_ability, (bit<32>)0);
                if (temp_multipath_ability == 0) {
                    // the node cannot multipath
                    ipv4_singlepath_lpm.apply();
                }
                else {
                    // the node can multipath
                    if (meta.packet_can_multipath == 1) {
                        // the packet can multipath
                        bit<32> temp2 = 0;
                        bit<32> temp3 = 0;
                        bit<32> temp4 = 0;
                        multipath_count.read(temp2, (bit<32>)2);
                        multipath_count.read(temp3, (bit<32>)3);
                        multipath_count.read(temp4, (bit<32>)4);
                        bit<32> ord2 = 0;
                        bit<32> ord3 = 0;
                        bit<32> ord4 = 0;
                        multipath_order.read(ord2, (bit<32>)2);
                        multipath_order.read(ord3, (bit<32>)3);
                        multipath_order.read(ord4, (bit<32>)4);
                        if (ord2 == 1) {
                            if (temp2 > 0) {
                                meta.multipath_port = 2;
                                temp2 = temp2 - 1;
                                multipath_count.write((bit<32>)2, temp2);
                            }
                            else {
                                if (ord3 == 2) {
                                    if (temp3 > 0) {
                                        meta.multipath_port = 3;
                                        temp3 = temp3 - 1;
                                        multipath_count.write((bit<32>)3, temp3);
                                    }
                                    else {
                                        if (temp4 > 0) {
                                            meta.multipath_port = 4;
                                            temp4 = temp4 - 1;
                                            multipath_count.write((bit<32>)4, temp4);
                                        }
                                    }
                                }
                                else if (ord4 == 2) {
                                    if (temp4 > 0) {
                                        meta.multipath_port = 4;
                                        temp4 = temp4 - 1;
                                        multipath_count.write((bit<32>)4, temp4);
                                    }
                                    else {
                                        if (temp3 > 0) {
                                            meta.multipath_port = 3;
                                            temp3 = temp3 - 1;
                                            multipath_count.write((bit<32>)3, temp3);
                                        }
                                    }
                                }
                            }
                        }
                        else if (ord3 == 1) {
                            if (temp3 > 0) {
                                meta.multipath_port = 3;
                                temp3 = temp3 - 1;
                                multipath_count.write((bit<32>)3, temp3);
                            }
                            else {
                                if (ord2 == 2) {
                                    if (temp2 > 0) {
                                        meta.multipath_port = 2;
                                        temp2 = temp2 - 1;
                                        multipath_count.write((bit<32>)2, temp2);
                                    }
                                    else {
                                        if (temp4 > 0) {
                                            meta.multipath_port = 4;
                                            temp4 = temp4 - 1;
                                            multipath_count.write((bit<32>)4, temp4);
                                        }
                                    }
                                }
                                else if (ord4 == 2) {
                                    if (temp4 > 0) {
                                        meta.multipath_port = 4;
                                        temp4 = temp4 - 1;
                                        multipath_count.write((bit<32>)4, temp4);
                                    }
                                    else {
                                        if (temp2 > 0) {
                                            meta.multipath_port = 2;
                                            temp2 = temp2 - 1;
                                            multipath_count.write((bit<32>)2, temp2);
                                        }
                                    }
                                }
                            }
                        }
                        else if (ord4 == 1) {
                            if (temp4 > 0) {
                                meta.multipath_port = 4;
                                temp4 = temp4 - 1;
                                multipath_count.write((bit<32>)4, temp4);
                            }
                            else {
                                if (ord2 == 2) {
                                    if (temp2 > 0) {
                                        meta.multipath_port = 2;
                                        temp2 = temp2 - 1;
                                        multipath_count.write((bit<32>)2, temp2);
                                    }
                                    else {
                                        if (temp3 > 0) {
                                            meta.multipath_port = 3;
                                            temp3 = temp3 - 1;
                                            multipath_count.write((bit<32>)3, temp3);
                                        }
                                    }
                                }
                                else if (ord3 == 2) {
                                    if (temp3 > 0) {
                                        meta.multipath_port = 3;
                                        temp3 = temp3 - 1;
                                        multipath_count.write((bit<32>)3, temp3);
                                    }
                                    else {
                                        if (temp2 > 0) {
                                            meta.multipath_port = 2;
                                            temp2 = temp2 - 1;
                                            multipath_count.write((bit<32>)2, temp2);
                                        }
                                    }
                                }
                            }
                        }
                        if (temp2 == 0) {
                            if (temp3 == 0) {
                                if (temp4 == 0) {
                                    multipath_initial.read(temp2, (bit<32>)2);
                                    multipath_initial.read(temp3, (bit<32>)3);
                                    multipath_initial.read(temp4, (bit<32>)4);
                                    multipath_count.write((bit<32>)2, temp2);
                                    multipath_count.write((bit<32>)3, temp3);
                                    multipath_count.write((bit<32>)4, temp4);
                                }
                            }
                        }
                        ipv4_multipath_lpm.apply();
                    }
                    else {
                        // the packet can not multipath
                        ipv4_singlepath_lpm.apply();
                    }
                }
            }
            else {
                // other packet should be forwarded singlepath
                ipv4_singlepath_lpm.apply();
            }
            if (temp_eccn == 1) {
                // the packet should be used eccn
            }
        }
        else {
            // is the packet for backstream
        }
    }
}
//------------------------------------------------------------
control c_egress(inout headers hdr, 
                 inout metadata meta, 
                 inout standard_metadata_t standard_metadata) {
    apply {
        //if (hdr.probe.isValid()) {
            // is the packet for int
        //}
    }
}
//------------------------------------------------------------
control c_compute_checksum(inout headers hdr,
                           inout metadata meta) {
    apply {

    }
}
//------------------------------------------------------------
control c_deparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.arp);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.icmp);
        packet.emit(hdr.tcp);
        packet.emit(hdr.udp);
    }
}
//------------------------------------------------------------
V1Switch(
    c_parser(),
    c_verify_checksum(),
    c_ingress(),
    c_egress(),
    c_compute_checksum(),
    c_deparser()
) main;