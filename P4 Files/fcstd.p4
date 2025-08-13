#include <core.p4>
#include <v1model.p4>

register<bit<32>>(1024) pkt_count_table;
register<bit<32>>(1024) byte_count_table;
register<bit<32>>(1024) flow_count_table;

control ingress {
    apply {
        bit<32> index = standard_metadata.ingress_port;
        bit<32> pkt_count;
        pkt_count_table.read(pkt_count, index);
        pkt_count = pkt_count + 1;
        pkt_count_table.write(index, pkt_count);

        bit<32> byte_count;
        byte_count_table.read(byte_count, index);
        byte_count = byte_count + standard_metadata.packet_length;
        byte_count_table.write(index, byte_count);

        // Extend here for more feature counters
    }
}

control egress { apply { } }

control MySwitch(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    apply { }
}

V1Switch(MyParser(),
         MyVerifyChecksum(),
         ingress(),
         egress(),
         MyComputeChecksum(),
         MyDeparser()) main;
