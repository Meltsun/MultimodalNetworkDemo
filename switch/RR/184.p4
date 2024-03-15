/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

#define MAX_PORTS 255
#define MAX_HOPS 127

const bit<16> ETH_TYPE_IPV4 = 0x0800;
const bit<16> ETH_TYPE_ARP = 0x0806;
const bit<48> VIRTUAL_MAC = 1;

//register< bit<32> >(8) register_count;

/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/
header ethernet_t {
    bit<48> dst_addr;
    bit<48> src_addr;
    bit<16> ether_type;
}
header arp_t {
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
header ipv4_t {
    bit<4>   version;
    bit<4>   header_length;
    bit<8>   service_type;
    bit<16>  total_length;
    bit<16>  identification;
    bit<3>   flags;
    bit<13>  frag_offset;
    bit<8>   ttl;
    bit<8>   protocol;
    bit<16>  header_checksum;
    bit<32>  src_ipv4;
    bit<32>  dst_ipv4; 
}
struct metadata {
    bit<32> temp_ip;
    bit<32> port;
}
struct headers {
    ethernet_t ethernet;
    ipv4_t ipv4;
    arp_t arp;
}
/*************************************************************************
*********************** P A R S E R  ***********************************
*************************************************************************/
parser c_parser(packet_in packet, out headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {
    state start {
        transition parse_ethernet;
    }
    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.ether_type) {
            ETH_TYPE_IPV4: parse_ipv4;
            ETH_TYPE_ARP: parse_arp;
            default: accept;
        }
    }
    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition accept;
    }
    state parse_arp {
        packet.extract(hdr.arp);
        transition accept;
    }
}
/*************************************************************************
************   C H E C K S U M    V E R I F I C A T I O N   *************
*************************************************************************/
control c_verify_checksum(inout headers hdr, inout metadata meta) {
    apply {}
}
/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/
control c_ingress(inout headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {
    //register< bit<9> >(16) register_ingress_packet_count;
    register< bit<32> >(4) input_port_pkt_count;
//---------------------------------------------------------------------------------------------
    action _drop() {
        mark_to_drop(standard_metadata);
    }

    //更新进入端口的数据包数量
    action update_input_port_pkt_count (in bit<9> ingress_port) {
        bit<32> pkt_count;
        // With P4_16 + v1model architecture, read a register using:
        // <register_instance_name>.read(<variable_where_value_read_is_stored>,
        //                               <index_to_read>);
        input_port_pkt_count.read(pkt_count, (bit<32>) ingress_port);
        pkt_count = pkt_count + 1;
        if (pkt_count > 3){
            pkt_count = pkt_count - 3;
        }
        // <register_instance_name>.write(<index_to_write>, <value_to_write>);
        input_port_pkt_count.write((bit<32>) ingress_port, pkt_count);
        meta.port = pkt_count;
    }
//----------------------------------------------------------------------------------------------

//-----------------------------------------------------------------------------------------------
    action to_port(bit<48> dst_addr, bit<9> port) {
        hdr.ethernet.src_addr = hdr.ethernet.dst_addr;
        hdr.ethernet.dst_addr = dst_addr;
        standard_metadata.egress_spec = port;  //下发流表来指定端口
    }

    table select_port_forward{
        key = {
            meta.port: exact;
        }
        actions = {
            to_port;
            _drop;
        }
        size = 1024;
        default_action = _drop();
    }
//------------------------------------------------------------------------------------------------

//------------------------------------------------------------------------------------------------
    action ipv4_forward(bit<48> src_addr, bit<48> dst_addr, bit<9> port) {
        hdr.ethernet.src_addr = src_addr;
        hdr.ethernet.dst_addr = dst_addr;        
        standard_metadata.egress_spec = port;
    }

    table ipv4_lpm {
        key = {
            hdr.ipv4.dst_ipv4: lpm;
        }
        actions = {
            ipv4_forward;
            _drop;
        }
        size = 1024;
        default_action = _drop();
    }
//--------------------------------------------------------------------------------------------------

    apply {
        if (hdr.arp.isValid()) {
            
            hdr.ethernet.dst_addr = hdr.ethernet.src_addr;
            hdr.ethernet.src_addr = VIRTUAL_MAC;

            hdr.arp.OPER = 2;

            meta.temp_ip = hdr.arp.sender_ip;
            
            hdr.arp.sender_ip = hdr.arp.target_ip;

            hdr.arp.target_ip = meta.temp_ip;
            hdr.arp.target_ha = hdr.arp.sender_ha;

            hdr.arp.sender_ha = VIRTUAL_MAC;
            
            standard_metadata.egress_spec = standard_metadata.ingress_port;
        }
        else {
            if (standard_metadata.ingress_port == 1){
                update_input_port_pkt_count(standard_metadata.ingress_port);

                select_port_forward.apply();
            }
            else{
                ipv4_lpm.apply();   
            }    
        }
    }

}
/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   ********************
*************************************************************************/
control c_egress(inout headers hdr, inout metadata meta, inout standard_metadata_t standard_metadata) {
    apply {
    }
}
/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   ***************
*************************************************************************/
control c_compute_checksum(inout headers  hdr,inout metadata meta) {
    apply {}
}
/*************************************************************************
***********************  D E P A R S E R  *******************************
*************************************************************************/
control c_deparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.arp);
        packet.emit(hdr.ipv4);
    }
}
/*************************************************************************
***********************  S W I T C H  *******************************
*************************************************************************/
V1Switch(
    c_parser(),
    c_verify_checksum(),
    c_ingress(),
    c_egress(),
    c_compute_checksum(),
    c_deparser()
) main;