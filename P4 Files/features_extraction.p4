#include <core.p4>
#include <v1model.p4>

// Registers for each feature
register<bit<32>>(1024) PTPW;   // Packet Throughput per Window
register<bit<32>>(1024) BPFW;   // Byte Pattern Frequency per Window
register<bit<32>>(1024) IPD;    // Inter-Packet Delay
register<bit<32>>(1024) FER;    // Flow Entropy Rate
register<bit<32>>(1024) FPS;    // Flows per Second
register<bit<32>>(1024) SAPR;   // Source Address Packet Ratio
register<bit<32>>(1024) TPW;    // Traffic Packet Window
register<bit<32>>(1024) BWU;    // Bandwidth Utilization
register<bit<32>>(1024) FA;     // Flow Anomalies
register<bit<32>>(1024) TPR;    // Traffic Packet Ratio
register<bit<32>>(1024) PIF;    // Packet Influx Frequency
register<bit<32>>(1024) TTLV;   // TTL Value Distribution
register<bit<32>>(1024) RTS;    // Rate of TCP SYN Packets
register<bit<32>>(1024) PER;    // Packet Error Rate
register<bit<32>>(1024) CDP;    // Concurrent Destination Ports
register<bit<32>>(1024) ATD;    // Avg. Time per Destination
register<bit<32>>(1024) URS;    // Unique Request Sources
register<bit<32>>(1024) ACPC;   // Avg. Control Packet Count
register<bit<32>>(1024) IPF;    // Inbound Packet Frequency
register<bit<32>>(1024) FPH;    // Flows per Host
register<bit<32>>(1024) BPP;    // Bytes per Packet

// Helper: Update a register
action update_reg(register<bit<32>>(1024) reg, bit<32> index, bit<32> inc) {
    bit<32> val;
    reg.read(val, index);
    val = val + inc;
    reg.write(index, val);
}

control ingress {
    apply {
        bit<32> idx = standard_metadata.ingress_port;

        update_reg(PTPW, idx, 1);
        update_reg(BPFW, idx, standard_metadata.packet_length);
        update_reg(IPD, idx, 0); // Needs timestamp delta tracking
        update_reg(FER, idx, 0); // Computed periodically via controller
        update_reg(FPS, idx, 1);
        update_reg(SAPR, idx, 1);
        update_reg(TPW, idx, 1);
        update_reg(BWU, idx, standard_metadata.packet_length);
        update_reg(FA, idx, 0);
        update_reg(TPR, idx, 1);
        update_reg(PIF, idx, 1);
        update_reg(TTLV, idx, hdr.ipv4.ttl);
        update_reg(RTS, idx, (hdr.tcp.syn == 1) ? 1 : 0);
        update_reg(PER, idx, 0);
        update_reg(CDP, idx, 1);
        update_reg(ATD, idx, 0);
        update_reg(URS, idx, 1);
        update_reg(ACPC, idx, 0);
        update_reg(IPF, idx, 1);
        update_reg(FPH, idx, 1);
        update_reg(BPP, idx, standard_metadata.packet_length);
    }
}

control egress { apply { } }

V1Switch(MyParser(),
         MyVerifyChecksum(),
         ingress(),
         egress(),
         MyComputeChecksum(),
         MyDeparser()) main;
