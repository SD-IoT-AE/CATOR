#include <core.p4>
#include <v1model.p4>

const bit<32> WINDOW_SIZE_DEFAULT = 1000; // default packets per window

header metadata_t {
    bit<32> pkt_count;
    bit<32> byte_count;
    bit<32> window_id;
}

metadata_t meta;

control ingress {
    apply {
        // Increment packet count for the current window
        meta.pkt_count = meta.pkt_count + 1;
        meta.byte_count = meta.byte_count + standard_metadata.packet_length;

        // Example: detect if window full
        if (meta.pkt_count >= WINDOW_SIZE_DEFAULT) {
            // Export features to controller / DYNEX
            // This can be done via digest or packet-out
            meta.pkt_count = 0;
            meta.byte_count = 0;
            meta.window_id = meta.window_id + 1;
        }
    }
}

control egress {
    apply { }
}

control MySwitch(inout headers hdr,
                 inout metadata_t meta,
                 inout standard_metadata_t standard_metadata) {
    apply { }
}

V1Switch(MyParser(),
         MyVerifyChecksum(),
         ingress(),
         egress(),
         MyComputeChecksum(),
         MyDeparser()) main;
