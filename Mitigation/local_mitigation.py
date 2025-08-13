class LocalMitigation:
    """
    Implements localized mitigation directly on the detecting switch.
    """

    def __init__(self, policies):
        self.policies = policies

    def apply(self, switch_id, flows, policy):
        """
        Applies the policy on the given switch for specified flows.
        """
        action = policy.get("action", None)
        rate_limit = policy.get("rate_limit", None)

        for flow in flows:
            if action == "drop":
                print(f"[LocalMitigation] Dropping flow {flow} on {switch_id}")
                # TODO: Install P4 table entry to drop packets for this flow
            elif action == "rate-limit":
                print(f"[LocalMitigation] Rate limiting flow {flow} to {rate_limit} on {switch_id}")
                # TODO: Install meter entry in P4 for rate limiting
            elif action == "redirect":
                print(f"[LocalMitigation] Redirecting flow {flow} to scrubber on {switch_id}")
                # TODO: Modify forwarding table entry
