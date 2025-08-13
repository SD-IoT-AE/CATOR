from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load mitigation policies
with open("config/mitigation_policies.json") as f:
    policies = json.load(f)["policies"]

@app.route("/mitigate", methods=["POST"])
def mitigate():
    data = request.get_json()
    attack_type = data.get("attack_type")
    flows = data.get("flows")

    policy = policies.get(attack_type, None)
    if not policy:
        return jsonify({"status": "error", "message": "No policy for attack type"}), 400

    # Apply mitigation (placeholder for P4/OpenFlow commands)
    for flow in flows:
        if policy["action"] == "drop":
            print(f"[DomainController] Dropping {flow}")
        elif policy["action"] == "rate-limit":
            print(f"[DomainController] Limiting {flow} to {policy['rate_limit']}")
        elif policy["action"] == "redirect":
            print(f"[DomainController] Redirecting {flow} to scrubber")

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6654)
