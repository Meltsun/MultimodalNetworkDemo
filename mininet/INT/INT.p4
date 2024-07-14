/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>
//------------------------------------------------------------
// 定义协议号
const bit<16> TYPE_IPV4 = 0x0800;
// const bit<16> TYPE_IPV6 = 0x86dd;
// const bit<16> TYPE_SINET = 0x8999;
// const bit<16> TYPE_ARP = 0x0806;
const bit<16> TYPE_PROBE = 0x0812;
// const bit<8>  IP_PROTO_TCP = 6;
// const bit<8>  IP_PROTO_UDP = 17;
// const bit<8>  IP_PROTO_ICMP = 1;

#define MAX_HOPS 20
#define MAX_PORTS 20

register<bit<32>>(MAX_PORTS) byte_cnt_reg; // 存储接口累积流量，INT协议使用
register<bit<48>>(MAX_PORTS) last_time_reg; // 存储上一个INT包到达时间，INT协议使用
register<bit<32>>(MAX_PORTS) encontpkts; // 存储出口数据包个数， INT协议使用
register<bit<32>>(MAX_PORTS) contpkts;
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
//header arp_h {
//    bit<16>  hardware_type;
//    bit<16>  protocol_type;
//    bit<8>   HLEN;
//    bit<8>   PLEN;
//    bit<16>  OPER;
//    bit<48>  sender_ha;
//    bit<32>  sender_ip;
//    bit<48>  target_ha;
//    bit<32>  target_ip;
//}
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
//IPv6首部
//header ipv6_h {
//    bit<4>    version;
//    bit<8>    traffic_class;
//    bit<20>   flow_label;
//    bit<16>   payload_len;
//    bit<8>    next_header;
//    bit<8>    hop_limit;
//    bit<128>  src_addr;
//    bit<128>  dst_addr;
//}
//--------------------------
//INT首部
header probe_h {
    bit<8>    hop_cnt; // probe_fwd字段个数
    bit<8>    data_cnt; // probe_data字段个数
}
//--------------------------
header probe_fwd_h {
    bit<8>   egress_spec; // 交换机端口标识
}
//--------------------------
header probe_data_h {
    bit<8>    swid; // 交换机标识
    bit<8>    port; // 端口号
    bit<32>   byte_cnt; // 流量
    bit<32>   pckcont; // 入口数据包个数
    bit<32>   enpckcont; // 出口数据包个数
    bit<48>   last_time; // 上一个INT包到达时间
    bit<48>   cur_time; // 当前INT包到达时间
    bit<48>   in_time; // 进端口记录时间
    bit<32>   qdepth; // 队列长度
}
//--------------------------
// ICMP首部
//header icmp_h {
//    bit<8>   type;
//    bit<8>   code;
//    bit<16>  hdr_checksum;
//}
//--------------------------
//SINET首部
//header sinet_h {
//    bit<4>   version;
//    bit<8>   slice_id;
//    bit<20>  flow_label;
//    bit<16>  payload_len;
//    bit<8>   src_id_len;
//    bit<8>   dst_id_len;
//    bit<32>  src_id;
//    bit<32>  dst_id;
//    bit<16>  protocol_id;
//    bit<8>   hop_limit;
//}
//--------------------------
//TCP首部
//header tcp_h {
//    bit<16>  src_port;
//    bit<16>  dst_port;
//    bit<32>  seq_no;
//    bit<32>  ack_no;
//    bit<4>   data_offset;
//    bit<4>   res;
//    bit<8>   flags;
//    bit<16>  window;
//    bit<16>  checksum;
//    bit<16>  urgent_ptr;
//}
//--------------------------
//UDP首部
//header udp_h {
//    bit<16>  src_port;
//    bit<16>  dst_port;
//    bit<16>  hdr_length;
//    bit<16>  checksum;
//}
//--------------------------
struct metadata {
    bit<8>   remaining1;
    bit<8>   remaining2;
    bit<8>   egress_spec;
    bit<8>   sswid;
    bit<32>  pktcont2;
    bit<48>  ingress_time;
}
//--------------------------
//完整首部
struct headers {
    ethernet_h               ethernet;
    //arp_h                    arp;
    ipv4_h                   ipv4;
    probe_h                  probe;
    probe_data_h[MAX_HOPS]   probe_data;
    probe_fwd_h[MAX_HOPS]    probe_fwd;
    //ipv6_h                   ipv6;
    //icmp_h                   icmp;
    //sinet_h                  sinet;
    //tcp_h                    tcp;
    //udp_h                    udp;
}
//------------------------------------------------------------
parser c_parser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start {
        transition parse_ethernet;
    }

    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.ether_type) {
            TYPE_IPV4: parse_ipv4;
            TYPE_PROBE: parse_probe;
            //TYPE_IPV6: parse_ipv6;
            //TYPE_SINET: parse_sinet;
            //TYPE_ARP: parse_arp;
            default: accept;
        }
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol) {
            //IP_PROTO_TCP: parse_tcp;
            //IP_PROTO_UDP: parse_udp;
            //IP_PROTO_ICMP: parse_icmp;
            default: accept;
        }
    }

    //state parse_tcp {
    //   packet.extract(hdr.tcp);
    //   transition accept;
    //}

    //state parse_udp {
    //   packet.extract(hdr.udp);
    //   transition accept;
    //}

    //state parse_icmp {
    //    packet.extract(hdr.icmp);
    //    transition accept;
    //}

    state parse_probe {
        packet.extract(hdr.probe);
        meta.remaining1 = hdr.probe.hop_cnt;
        meta.remaining2 = hdr.probe.data_cnt;
        transition select(hdr.probe.data_cnt) {
            0: parse_probe_fwd;
            default: parse_probe_data;
        }
    }

    state parse_probe_data {
        packet.extract(hdr.probe_data.next);
        meta.remaining2 = meta.remaining2 - 1;
        transition select(meta.remaining2) {
            0: parse_probe_fwd;
            default: parse_probe_data;
        }
    }

    state parse_probe_fwd {
        packet.extract(hdr.probe_fwd.next);
        meta.remaining1 = meta.remaining1 - 1;
        transition select(meta.remaining1) {
            0: accept;
            default: parse_probe_fwd;
        }
    }

    //state parse_ipv6 {
    //    packet.extract(hdr.ipv6);
    //    transition accept;
    //}

    //state parse_sinet {
    //    packet.extract(hdr.sinet);
    //    transition accept;
    //}

    //state parse_arp {
    //    packet.extract(hdr.arp);
    //    transition accept;
    //}
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
    action drop() {
        mark_to_drop(standard_metadata);
    }

    action ipv4_forward(bit<48> dst_mac, bit<9> port) {
        hdr.ethernet.src_mac = hdr.ethernet.dst_mac;
        hdr.ethernet.dst_mac = dst_mac;
        standard_metadata.egress_spec = port;
    }

    table ipv4_lpm {
        key = {
            // hdr.ipv4.dst_addr: exact;
            hdr.ipv4.dst_addr: lpm;
        }
        actions = {
            ipv4_forward;
            drop;
        }
        size = 1024;
        default_action = drop();
    }

    action set_swid1(bit<8> swid) {
        meta.sswid = swid;
    }

    table swid1 {
        actions = {
            set_swid1;
            NoAction;
        }
        default_action = NoAction();
    }

    apply {
    bit<32> contpp;
    bit<32> new_cont;
        //if (hdr.arp.isValid()) {
            //deal with arp packet
        //    if (hdr.arp.target_ip == 0x0a0a0101) {
                //ask who is 10.10.1.1
        //        hdr.ethernet.dst_mac = hdr.ethernet.src_mac;
        //        hdr.ethernet.src_mac = 0x00000a0a0101;
        //        hdr.arp.OPER = 2;
        //        hdr.arp.target_ha = hdr.arp.sender_ha;
        //        hdr.arp.target_ip = hdr.arp.sender_ip;
        //        hdr.arp.sender_ip = 0x0a0a0101;
        //        hdr.arp.sender_ha = 0x00000a0a0101;
        //        standard_metadata.egress_spec = standard_metadata.ingress_port;
        //    }
        //}
	meta.ingress_time=standard_metadata.ingress_global_timestamp;
// ingress packet conut--   increment byte cnt for this packet's port
        contpkts.read(contpp, (bit<32>)standard_metadata.ingress_port);
	contpp = contpp + 1;
        meta.pktcont2=contpp;  //trans to egress packetdata
	    // reset the byte count when a probe packet passes through
	new_cont = (hdr.probe.isValid()) ? 0 : contpp;
	contpkts.write((bit<32>)standard_metadata.ingress_port, new_cont); 
        swid1.apply();
        if (hdr.probe.isValid()) {
            standard_metadata.egress_spec = (bit<9>)hdr.probe_fwd[0].egress_spec;
            hdr.probe.hop_cnt = hdr.probe.hop_cnt - 1; 
            hdr.probe_fwd.pop_front(1);
        }
        else if (hdr.ipv4.isValid()) {
            ipv4_lpm.apply();
        }
    }
}
//------------------------------------------------------------
control c_egress(inout headers hdr, 
                 inout metadata meta, 
                 inout standard_metadata_t standard_metadata) {
    
     action set_swid(bit<8> swid) {
        hdr.probe_data[0].swid = swid;
    }

     table swid {
        actions = {
            set_swid;
            NoAction;
        }
        default_action = NoAction();
    }

    apply {
        bit<32> encontpp;
        bit<32> new_encont;
        encontpkts.read(encontpp, (bit<32>)standard_metadata.egress_port);
	encontpp = encontpp + 1;  //ingress端口计数
        new_encont = (hdr.probe.isValid()) ? 0 : encontpp;
	encontpkts.write((bit<32>)standard_metadata.egress_port, new_encont);  //有探测包经过时，重置计数
        
        bit<32> byte_cnt;
        bit<32> new_byte_cnt;
        bit<48> last_time;
        bit<48> cur_time = standard_metadata.egress_global_timestamp;
        byte_cnt_reg.read(byte_cnt, (bit<32>)standard_metadata.egress_port);
        byte_cnt = byte_cnt + standard_metadata.packet_length;  //端口出包计数
        new_byte_cnt = (hdr.probe.isValid()) ? 0 : byte_cnt;
        byte_cnt_reg.write((bit<32>)standard_metadata.egress_port, new_byte_cnt);  //有探测包经过时，重置计数
        if (hdr.probe.isValid()) {
            hdr.probe_data.push_front(1);
	    hdr.probe_data[0].setValid(); 
            // 设置swid ID 字段
            swid.apply();
            hdr.probe_data[0].port = (bit<8>)standard_metadata.egress_port;
            hdr.probe_data[0].byte_cnt = byte_cnt;
            hdr.probe_data[0].pckcont =meta.pktcont2;
	    hdr.probe_data[0].enpckcont =encontpp;
            // 读取和更新 last_time 寄存器
            last_time_reg.read(last_time, (bit<32>)standard_metadata.egress_port);
            last_time_reg.write((bit<32>)standard_metadata.egress_port, cur_time);
            hdr.probe_data[0].last_time = last_time;
            hdr.probe_data[0].cur_time = cur_time;
            hdr.probe_data[0].in_time = meta.ingress_time;
            hdr.probe_data[0].qdepth = (bit<32>)standard_metadata.deq_qdepth;
            hdr.probe.data_cnt =hdr.probe.data_cnt + 1;
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
        //packet.emit(hdr.arp);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.probe);
        packet.emit(hdr.probe_data);
        packet.emit(hdr.probe_fwd);
        //packet.emit(hdr.ipv6);
        //packet.emit(hdr.icmp);
        //packet.emit(hdr.sinet);
        //packet.emit(hdr.tcp);
        //packet.emit(hdr.udp);
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
