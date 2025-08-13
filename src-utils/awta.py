import json
import time
import numpy as np
from utils.entropy import compute_entropy, compute_mdr
from utils.p4_interface import P4Interface
from dtw import DTW
from dynex import DYNEX

class AWTA:
    def __init__(self, config_path, p4_config, dynex_model):
        with open(config_path) as f:
            cfg = json.load(f)
        self.entropy_thresholds = cfg["entropy_thresholds"]
        self.dtw_cfg = cfg["dtw"]

        with open(p4_config) as f:
            self.p4_cfg = json.load(f)

        self.switches = []
        for sw in self.p4_cfg["switches"]:
            iface = P4Interface(
                p4info_path="p4/features_extraction.p4info",
                bmv2_json_path="p4/features_extraction.json",
                grpc_addr=sw["grpc_addr"],
                device_id=0
            )
            iface.set_pipeline()
            self.switches.append((sw, iface))

        self.dtw = DTW(
            theta_min=self.entropy_thresholds["theta_min"],
            theta_max=self.entropy_thresholds["theta_max"],
            min_window=self.dtw_cfg["min_window"],
            max_window=self.dtw_cfg["max_window"],
            delta=self.dtw_cfg["delta"]
        )

        self.dynex = dynex_model

    def _pull_features(self, iface, feature_list):
        """Pull all features from P4 registers."""
        feature_vector = []
        for feature in feature_list:
            values = iface.read_register_all(feature, 1)  # Assuming single index per port
            feature_vector.append(np.mean(values))  # Aggregate across ports
        return np.array(feature_vector).reshape(1, -1)

    def monitor(self):
        """Main AWTA loop."""
        while True:
            for sw, iface in self.switches:
                features = self._pull_features(iface, sw["feature_set"])

                # Example: Compute entropy from packet count distribution
                packet_counts = iface.read_register_all("PTPW", 1)
                entropy_val = compute_entropy(packet_counts)

                # Compute MDR (needs baseline entropy)
                mdr = compute_mdr(packet_counts, baseline_entropy=1.0)  # Placeholder baseline
                new_window = self.dtw.adjust_window(mdr)

                print(f"[AWTA] Switch {sw['id']} Window: {new_window} Entropy: {entropy_val:.4f} MDR: {mdr:.4f}")

                # Classify traffic with DYNEX
                label = self.dynex.predict(features)
                if label == 1:
                    print(f"[ALERT] DDoS detected on {sw['id']}!")
                    # In a real system, pass to ACM for mitigation

            time.sleep(self.dtw.current_window)
