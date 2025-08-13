import grpc
import p4runtime_lib.helper
from p4runtime_lib.switch import ShutdownAllSwitchConnections

class P4Interface:
    """
    Handles communication with P4 switches over gRPC.
    Allows reading/writing registers, counters, and setting table entries.
    """
    def __init__(self, p4info_path, bmv2_json_path, grpc_addr, device_id=0):
        self.p4info_path = p4info_path
        self.bmv2_json_path = bmv2_json_path
        self.grpc_addr = grpc_addr
        self.device_id = device_id
        self.helper = p4runtime_lib.helper.P4InfoHelper(p4info_path)
        self.client = self._connect()

    def _connect(self):
        print(f"[P4Interface] Connecting to {self.grpc_addr}...")
        return self.helper.buildSwitchConnection(
            name=f"sw{self.device_id}",
            address=self.grpc_addr,
            device_id=self.device_id,
            proto_dump_file=f"logs/p4runtime-sw{self.device_id}.txt"
        )

    def set_pipeline(self):
        """Push the P4 program to the switch."""
        print(f"[P4Interface] Installing pipeline {self.bmv2_json_path}...")
        self.client.MasterArbitrationUpdate()
        self.client.SetForwardingPipelineConfig(
            p4info=self.helper.p4info,
            bmv2_json_file_path=self.bmv2_json_path
        )

    def read_register(self, reg_name, index):
        """Read a single register value from the P4 switch."""
        reg_id = self.helper.get_register_id(reg_name)
        for response in self.client.ReadRegisters(reg_id, index):
            for entity in response.entities:
                return entity.register_entry.data.uint64
        return None

    def read_register_all(self, reg_name, size):
        """Read all register values from the P4 switch."""
        values = []
        for i in range(size):
            values.append(self.read_register(reg_name, i))
        return values

    def write_register(self, reg_name, index, value):
        """Write a value to a register."""
        reg_id = self.helper.get_register_id(reg_name)
        self.client.WriteRegister(reg_id, index, value)

    def shutdown(self):
        ShutdownAllSwitchConnections()
