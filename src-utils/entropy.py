import numpy as np

def compute_entropy(counts):
    """Shannon entropy calculation."""
    total = sum(counts)
    if total == 0:
        return 0.0
    probs = [c/total for c in counts if c > 0]
    return -sum(p * np.log2(p) for p in probs)

def compute_mdr(counts, baseline_entropy):
    """Mean Decline Ratio (MDR) calculation."""
    attack_entropy = compute_entropy(counts)
    if baseline_entropy == 0:
        return 0.0
    nadir = baseline_entropy - attack_entropy
    return nadir / baseline_entropy
