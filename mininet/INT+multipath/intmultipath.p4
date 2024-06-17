/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>
//------------------------------------------------------------
// 定义协议号
const bit<16> TYPE_ARP = 0x0806;
const bit<16> TYPE_PROBE = 0x0812;
const bit<16> TYPE_IPV4 = 0x0800;
const bit<8>  IP_PROTO_ICMP = 0x01;
const bit<8>  IP_PROTO_TCP = 0x06;
const bit<8>  IP_PROTO_UDP = 0x11;

#define MAX_HOPS 10
#define MAX_PORTS 10

register< bit<32> >(8) transmition_model;
// 共8个寄存器，索引为32位，每个寄存器存一个32位的数
// transmition_model[0]=1，则使用ECCN，=0则不用
// transmition_model[1]=1，则使用多路径，=0则不用

register< bit<32> >(8) multipath_ability;
// 共8个寄存器，索引为32位，每个寄存器存一个32位的数
// multipath_ability[0]=1，则支持多路径，=0则不支持
register< bit<32> >(8) multipath_count; 
// 共8个寄存器，索引为32位，每个寄存器存32位的数
// multipath_count[2,3,4]分别代表端口2,3,4的发包量
register< bit<32> >(8) multipath_initial;
// 共8个寄存器，索引为32位，每个寄存器存32位的数
// multipath_initial[2,3,4]分别代表端口2,3,4的发包初始量
register< bit<32> >(8) multipath_order;
// 共8个寄存器，索引为32位，每个寄存器存32位的数
// multipath_order[2,3,4]分别代表端口2,3,4的发包顺序

register<bit<32>>(MAX_PORTS) int_byte_ingress; 
// 共MAX_PORTS个寄存器，索引为32位，每个寄存器存32位的数
// 存储端口累积入流量，INT协议使用，int_byte_ingress[1]代表端口1的累计入流量
register<bit<32>>(MAX_PORTS) int_byte_egress; 
// 共MAX_PORTS个寄存器，索引为32位，每个寄存器存32位的数
// 存储端口累积出流量，INT协议使用，int_byte_egress[1]代表端口1的累计出流量
register<bit<32>>(MAX_PORTS) int_count_ingress;
// 共MAX_PORTS个寄存器，索引为32位，每个寄存器存32位的数
// 存储端口累积入个数，INT协议使用，int_count_ingress[1]代表端口1的累计入个数
register<bit<32>>(MAX_PORTS) int_count_egress;
// 共MAX_PORTS个寄存器，索引为32位，每个寄存器存32位的数
// 存储端口累积出个数，INT协议使用，int_count_egress[1]代表端口1的累计出个数
register<bit<48>>(MAX_PORTS) int_last_time_ingress; 
// 共MAX_PORTS个寄存器，索引为32位，每个寄存器存48位的数
// 存储上一个INT包进入端口时间，INT协议使用，int_last_time_ingress[1]代表端口1的入INT包时间
register<bit<48>>(MAX_PORTS) int_last_time_egress; 
// 共MAX_PORTS个寄存器，索引为32位，每个寄存器存48位的数
// 存储上一个INT包离开出端口时间，INT协议使用，int_last_time_egress[1]代表端口1的出INT包时间

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
//INT首部
header probe_h {
    bit<8>    hop_cnt; // probe_fwd字段个数
    bit<8>    data_cnt; // probe_data字段个数
}
header probe_fwd_h {
    bit<8>   swid; // 交换机端口标识
}
header probe_data_h {
    bit<8>    swid; // 交换机标识
    bit<8>    port_ingress; // 入端口号
    bit<8>    port_egress; // 出端口号
    bit<32>   byte_ingress; // 入端口累计入流量
    bit<32>   byte_egress; // 出端口累计出流量
    bit<32>   count_ingress; // 入端口累计入个数
    bit<32>   count_egress; // 出端口累计出个数
    bit<48>   last_time_ingress; // 入端口上一个INT包进入时间
    bit<48>   last_time_egress; // 出端口上一个INT包离开时间
    bit<48>   current_time_ingress; // 入端口当前INT包进入时间
    bit<48>   current_time_egress; // 出端口当前INT包离开时间
    bit<32>   qdepth; // 队列长度
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
    bit<8> int_hop_cnt;
    bit<8> int_data_cnt;
}
//--------------------------
//完整首部
struct headers {
    ethernet_h               ethernet;
    arp_h                    arp;
    probe_h                  probe;
    probe_fwd_h[MAX_HOPS]    probe_fwd;
    probe_data_h[MAX_HOPS]   probe_data;
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
        meta = {0, 0, 0, 0};
        transition parse_ethernet;
    }
    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.ether_type) {
            TYPE_ARP: parse_arp;
            TYPE_PROBE: parse_probe;
            TYPE_IPV4: parse_ipv4;
            default: accept;
        }
    }
    state parse_arp {
        packet.extract(hdr.arp);
        transition accept;
    }
    state parse_probe {
        packet.extract(hdr.probe);
        meta.int_hop_cnt = hdr.probe.hop_cnt;
        meta.int_data_cnt = hdr.probe.data_cnt;
        transition parse_probe_fwd_h;
    }
    state parse_probe_fwd_h {
        transition select(meta.int_hop_cnt) {
            0: parse_probe_data_h;
            default: parse_probe_fwd;
        }
    }
    state parse_probe_fwd {
        packet.extract(hdr.probe_fwd.next);
        meta.int_hop_cnt = meta.int_hop_cnt - 1;
        transition select(meta.int_hop_cnt) {
            0: parse_probe_data_h;
            default: parse_probe_fwd;
        }
    }
    state parse_probe_data_h {
        transition select(meta.int_data_cnt) {
            0: accept;
            default: parse_probe_data;
        }
    }
    state parse_probe_data {
        packet.extract(hdr.probe_data.next);
        meta.int_data_cnt = meta.int_data_cnt - 1;
        transition select(meta.int_data_cnt) {
            0: accept;
            default: parse_probe_data;
        }
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
    action probe_forward(bit<48> src_mac, bit<48> dst_mac, bit<9> port) {
        hdr.ethernet.src_mac = src_mac;
        hdr.ethernet.dst_mac = dst_mac;
        standard_metadata.egress_spec = port;
    }
    table probe_exact {
        key = {
            hdr.probe_fwd[0].swid: exact;
        }
        actions = {
            probe_forward;
            _drop;
        }
        size = 1024;
        default_action = _drop();
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
                hdr.ethernet.src_mac = 0x000000000176;
                hdr.arp.OPER = 2;
                hdr.arp.target_ha = hdr.arp.sender_ha;
                hdr.arp.target_ip = hdr.arp.sender_ip;
                hdr.arp.sender_ip = 0x0aaaaa01;
                hdr.arp.sender_ha = 0x000000000176;
                standard_metadata.egress_spec = standard_metadata.ingress_port;
            }
            else if (hdr.arp.target_ip == 0x0ab4b401) {
                //ask who is 10.180.180.1
                hdr.ethernet.dst_mac = hdr.ethernet.src_mac;
                hdr.ethernet.src_mac = 0x000000000180;
                hdr.arp.OPER = 2;
                hdr.arp.target_ha = hdr.arp.sender_ha;
                hdr.arp.target_ip = hdr.arp.sender_ip;
                hdr.arp.sender_ip = 0x0ab4b401;
                hdr.arp.sender_ha = 0x000000000180;
                standard_metadata.egress_spec = standard_metadata.ingress_port;
            }
        }
        else if (hdr.probe.isValid()) {
            // is the packet for int
            hdr.probe.data_cnt = hdr.probe.data_cnt + 1;
            hdr.probe_data.push_front(1);
            hdr.probe_data[0].setValid(); 
            hdr.probe_data[0].swid = hdr.probe_fwd[0].swid; // 存入swid
            hdr.probe_data[0].port_ingress = (bit<8>)standard_metadata.ingress_port; // 存入入端口号
            bit<32> temp_byte_ingress = 0;
            int_byte_ingress.read(temp_byte_ingress, (bit<32>)standard_metadata.ingress_port); // 读取入端口累计入流量
            hdr.probe_data[0].byte_ingress = temp_byte_ingress; // 存入入端口累计入流量
            temp_byte_ingress = 0; // 累加入流量清零
            int_byte_ingress.write((bit<32>)standard_metadata.ingress_port, temp_byte_ingress); // 存入新累计入流量
            bit<32> temp_count_ingress = 0;
            int_count_ingress.read(temp_count_ingress, (bit<32>)standard_metadata.ingress_port); // 读取入端口累计入数量
            hdr.probe_data[0].count_ingress = temp_count_ingress; // 存入入端口累计入数量
            temp_count_ingress = 0; // 累加入数量清零
            int_count_ingress.write((bit<32>)standard_metadata.ingress_port, temp_count_ingress); // 存入新累计入数量
            bit<48> temp_last_time_ingress = 0;
            int_last_time_ingress.read(temp_last_time_ingress, (bit<32>)standard_metadata.ingress_port); // 读取入端口上一个INT包进入时间
            hdr.probe_data[0].last_time_ingress = temp_last_time_ingress; // 存入入端口上一个INT包进入时间
            temp_last_time_ingress = standard_metadata.ingress_global_timestamp; // 更新上一个INT包进入时间
            int_last_time_ingress.write((bit<32>)standard_metadata.ingress_port, temp_last_time_ingress);  // 存入新上一个INT包进入时间
            hdr.probe_data[0].current_time_ingress = standard_metadata.ingress_global_timestamp;  // 存入入端口当前INT包进入时间

            hdr.probe.hop_cnt = hdr.probe.hop_cnt - 1;
            hdr.probe_fwd.pop_front(1);
            probe_exact.apply();
        }
        else if (ipv4_is_for_video.apply().hit) {
            // is the packet for video
            // int first
            bit<32> temp_byte_ingress = 0;
            int_byte_ingress.read(temp_byte_ingress, (bit<32>)standard_metadata.ingress_port); // 读取入端口累计入流量
            temp_byte_ingress = temp_byte_ingress + standard_metadata.packet_length; // 累加当前入流量
            int_byte_ingress.write((bit<32>)standard_metadata.ingress_port, temp_byte_ingress); // 存入新累计入流量
            bit<32> temp_count_ingress = 0;
            int_count_ingress.read(temp_count_ingress, (bit<32>)standard_metadata.ingress_port); // 读取入端口累计入数量
            temp_count_ingress = temp_count_ingress + 1; // 累加1
            int_count_ingress.write((bit<32>)standard_metadata.ingress_port, temp_count_ingress); // 存入新累计入数量

            // multipath second
            bit<32> temp_eccn = 0;
            bit<32> temp_multipath = 0;
            transmition_model.read(temp_eccn, (bit<32>)0);
            transmition_model.read(temp_multipath, (bit<32>)1);
            if (temp_multipath == 1 && (hdr.tcp.isValid() || hdr.icmp.isValid())) {
                // the tcp packet should be forwarded multipath
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

            // eccn last
            if (temp_eccn == 1) {
                // the packet should be used eccn
            }

        }
        else {
            // is the packet for backstream
            // int first
            bit<32> temp_byte_ingress = 0;
            int_byte_ingress.read(temp_byte_ingress, (bit<32>)standard_metadata.ingress_port); // 读取入端口累计入流量
            temp_byte_ingress = temp_byte_ingress + standard_metadata.packet_length; // 累加当前入流量
            int_byte_ingress.write((bit<32>)standard_metadata.ingress_port, temp_byte_ingress); // 存入新累计入流量
            bit<32> temp_count_ingress = 0;
            int_count_ingress.read(temp_count_ingress, (bit<32>)standard_metadata.ingress_port); // 读取入端口累计入数量
            temp_count_ingress = temp_count_ingress + 1; // 累加1
            int_count_ingress.write((bit<32>)standard_metadata.ingress_port, temp_count_ingress); // 存入新累计入数量
        }
    }
}
//------------------------------------------------------------
control c_egress(inout headers hdr, 
                 inout metadata meta, 
                 inout standard_metadata_t standard_metadata) {
    apply {
        if (hdr.arp.isValid()) {
            // is the packet for arp
        }
        else if (hdr.probe.isValid()) {
            // is the packet for int
            hdr.probe_data[0].port_egress = (bit<8>)standard_metadata.egress_spec; // 存入出端口号
            bit<32> temp_byte_egress = 0;
            int_byte_egress.read(temp_byte_egress, (bit<32>)standard_metadata.egress_spec); // 读取出端口累计出流量
            hdr.probe_data[0].byte_egress = temp_byte_egress; // 存入出端口累计出流量
            temp_byte_egress = 0; // 累加出流量清零
            int_byte_egress.write((bit<32>)standard_metadata.egress_spec, temp_byte_egress); // 存入新累计出流量
            bit<32> temp_count_egress = 0;
            int_count_egress.read(temp_count_egress, (bit<32>)standard_metadata.egress_spec); // 读取出端口累计出数量
            hdr.probe_data[0].count_egress = temp_count_egress; // 存入出端口累计出数量
            temp_count_egress = 0; // 累加出数量清零
            int_count_egress.write((bit<32>)standard_metadata.egress_spec, temp_count_egress); // 存入新累计出数量
            bit<48> temp_last_time_egress = 0;
            int_last_time_egress.read(temp_last_time_egress, (bit<32>)standard_metadata.egress_spec); // 读取出端口上一个INT包进出时间
            hdr.probe_data[0].last_time_egress = temp_last_time_egress; // 存入出端口上一个INT包进出时间
            temp_last_time_egress = standard_metadata.egress_global_timestamp; // 更新上一个INT包进出时间
            int_last_time_egress.write((bit<32>)standard_metadata.egress_spec, temp_last_time_egress);  // 存入新上一个INT包进出时间
            hdr.probe_data[0].current_time_egress = standard_metadata.egress_global_timestamp;  // 存入出端口当前INT包进出时间
            hdr.probe_data[0].qdepth = (bit<32>)standard_metadata.deq_qdepth; // 存入队列深度
        }
        else {
            // is the packet for video or backstream
            // int last
            bit<32> temp_byte_egress = 0;
            int_byte_egress.read(temp_byte_egress, (bit<32>)standard_metadata.egress_spec); // 读取出端口累计出流量
            temp_byte_egress = temp_byte_egress + standard_metadata.packet_length; // 累加当前出流量
            int_byte_egress.write((bit<32>)standard_metadata.egress_spec, temp_byte_egress); // 存出新累计出流量
            bit<32> temp_count_egress = 0;
            int_count_egress.read(temp_count_egress, (bit<32>)standard_metadata.egress_spec); // 读取出端口累计出数量
            temp_count_egress = temp_count_egress + 1; // 累加1
            int_count_egress.write((bit<32>)standard_metadata.egress_spec, temp_count_egress); // 存出新累计出数量
        }
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
        packet.emit(hdr.probe);
        packet.emit(hdr.probe_fwd);
        packet.emit(hdr.probe_data);
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