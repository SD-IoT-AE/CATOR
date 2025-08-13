import json
from mitigation.local_mitigation import LocalMitigation
from mitigation.distributed_mitigation import DistributedMitigation

class ACM:
    """
    Adaptive Cooperative Mitigation (ACM) orchestrator.
    Selects between local and distributed mitigation strategies
    depending on the network configuration and attack type.
    """

    def __init__(self, mitigation_config, controller_config):
        with open(mitigation_config) as f:
            self.policies = json.load(f)["policies"]

        with open(controller_config) as f:
            self.controllers = json.load(f)["controllers"]

        self.local_mitigator = LocalMitigation(self.policies)
        self.distributed_mitigator = DistributedMitigation(self.policies, self.controllers)

    def handle_alert(self, attack_type, src_switch, affected_flows):
        """
        Decides mitigation strategy based on attack type and topology.
        """
        policy = self.policies.get(attack_type, None)
        if not policy:
            print(f"[ACM] No policy for attack type {attack_type}, ignoring.")
            return

        if len(self.controllers) == 1:
            print(f"[ACM] Single controller setup: applying local mitigation on {src_switch}")
            self.local_mitigator.apply(src_switch, affected_flows, policy)
        else:
            print(f"[ACM] Multi-controller setup: applying distributed mitigation.")
            self.distributed_mitigator.apply(src_switch, affected_flows, policy)
