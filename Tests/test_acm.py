import unittest
from src.acm import ACM

class TestACM(unittest.TestCase):

    def test_handle_alert_local(self):
        acm = ACM("config/mitigation_policies.json", "config/controller_config.json")
        acm.local_mitigator.apply = lambda sw, flows, policy: print("Local mitigation called")
        acm.handle_alert("ddos", "s1", ["flow1"])

    def test_handle_alert_distributed(self):
        acm = ACM("config/mitigation_policies.json", "config/controller_config.json")
        acm.controllers.append({"id": "c2", "role": "domain", "ip": "127.0.0.1", "port": 6655})
        acm.distributed_mitigator.apply = lambda sw, flows, policy: print("Distributed mitigation called")
        acm.handle_alert("ddos", "s1", ["flow1"])

if __name__ == "__main__":
    unittest.main()
