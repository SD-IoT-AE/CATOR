from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
import json
import requests

class CentralController(app_manager.RyuApp):
    """
    Central Orchestration Controller (C0) – maintains network-wide policies
    and coordinates domain controllers for mitigation.
    """
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(CentralController, self).__init__(*args, **kwargs)
        with open("config/controller_config.json") as f:
            self.controllers = json.load(f)["controllers"]
        with open("config/mitigation_policies.json") as f:
            self.policies = json.load(f)["policies"]

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Install default table-miss flow entry
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
        self.logger.info("Installed table-miss flow on switch %s", datapath.id)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority, match=match, instructions=inst)
        datapath.send_msg(mod)

    def trigger_mitigation(self, attack_type, flows):
        """
        Instruct all domain controllers to mitigate.
        """
        for ctrl in self.controllers:
            if ctrl["role"] == "domain":
                url = f"http://{ctrl['ip']}:{ctrl['port']}/mitigate"
                try:
                    requests.post(url, json={
                        "attack_type": attack_type,
                        "flows": flows
                    })
                    self.logger.info("Sent mitigation request to %s", ctrl["id"])
                except Exception as e:
                    self.logger.error("Failed to contact %s: %s", ctrl["id"], e)
