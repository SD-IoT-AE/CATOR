import time
import requests
import json

class FailoverHandler:
    """
    Monitors controller health and promotes backup controllers if needed.
    """

    def __init__(self, controller_config):
        with open(controller_config) as f:
            self.controllers = json.load(f)["controllers"]

    def monitor(self):
        while True:
            for ctrl in self.controllers:
                url = f"http://{ctrl['ip']}:{ctrl['port']}/health"
                try:
                    r = requests.get(url, timeout=1)
                    if r.status_code == 200:
                        print(f"[Failover] {ctrl['id']} is alive.")
                    else:
                        self._trigger_failover(ctrl)
                except requests.exceptions.RequestException:
                    self._trigger_failover(ctrl)
            time.sleep(5)

    def _trigger_failover(self, failed_ctrl):
        print(f"[Failover] Controller {failed_ctrl['id']} is down! Triggering backup...")
        # TODO: Elect a new controller and update switch connections dynamically
