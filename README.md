# 🚀 CATOR: A Confidence-Adaptive Dual-Plane In-Switch Orchestrated Resilience Framework for Multi-Vector DDoS Defense in Software-Defined IoT

## 📌 Overview
CATOR is a **P4-enabled**, **machine-learning-driven**, and **multi-layered** framework for detecting and mitigating **sequential, multi-vector, and varying-intensity DDoS attacks** in **Software-Defined IoT (SD-IoT)** environments.  
It delivers **triple-category detection** (binary, multi-class, and multi-scenario), supports **multi-controller failover resilience**, and integrates in-switch intelligence for **low-latency** and **high-accuracy** defense.

**Core Modules**:
- **AWTA** – *Adaptive Window-based Traffic Analysis* (in-switch stateful monitoring with Fully Connected State Tables)
- **DTW** – *Dynamic Time-based Windowing* (entropy-driven adaptive detection intervals)
- **DYNEX** – *Dynamic Ensemble Classifier with Confidence Optimization*
- **ACM** – *Adaptive Cooperative Mitigation* (local + distributed mitigation)
- **Multi-Controller SDN** – Central + domain controllers for scalability & fault tolerance

---

## 📁 Project Structure

```
CATOR/
│
├── README.md                     # Overview, installation, usage
├── LICENSE                       # Open-source license
├── requirements.txt              # Python dependencies
├── config/
│   ├── cator_config.json         # Global parameters, thresholds
│   ├── datasets_config.json      # Paths & preprocessing configs for datasets
│   ├── p4_switch_config.json     # Switch IDs, ports, feature extraction rules
│   ├── controller_config.json    # Multi-controller setup parameters
│   ├── mitigation_policies.json  # ACM rate-limits, drop rules
│
├── p4/
│   ├── awta.p4                   # Adaptive Window-based Traffic Analysis (P4 program)
│   ├── fcstd.p4                  # Fully Connected State Table implementation
│   ├── features_extraction.p4    # Extraction of the 21 listed features
│
├── src/
│   ├── __init__.py
│   ├── dtw.py                    # Dynamic Time-based Windowing (entropy & MDR logic)
│   ├── awta.py                   # Python-side AWTA control & integration with P4
│   ├── dynex.py                  # Dynamic Ensemble with Confidence Optimization
│   ├── acm.py                    # Adaptive Cooperative Mitigation logic
│   ├── utils/
│   │   ├── entropy.py            # Shannon entropy, MDR calculations
│   │   ├── feature_selection.py  # Variance filtering, RFE
│   │   ├── metrics.py            # DA, F1, MCC, ATRT, etc.
│   │   ├── p4_interface.py       # API to communicate with P4 switches
│
├── controllers/
│   ├── central_controller.py     # C0 orchestration & policy distribution
│   ├── domain_controller.py      # C1, C2 domain handling
│   ├── failover_handler.py       # Backup controller logic
│
├── datasets/
│   ├── preprocessing.py          # Dataset preprocessing (CICIoT2023, ToN-IoT, etc.)
│   ├── loaders.py                # Loaders for training/testing
│
├── training/
│   ├── train_dynex.py            # Training pipeline for ensemble + ANN meta-learner
│   ├── eval_dynex.py             # Evaluation on datasets
│
├── mitigation/
│   ├── local_mitigation.py       # Algorithm 3.1 implementation
│   ├── distributed_mitigation.py # Algorithm 3.2 implementation
│
├── deployment/
│   ├── mininet_topology.py       # Mininet-WiFi/P4 testbed setup
│   ├── start_controllers.sh      # Script to start multi-controller system
│   ├── deploy_p4_switches.sh     # Deploy AWTA/FCSTD P4 programs
│
└── tests/
    ├── test_dtw.py
    ├── test_awta.py
    ├── test_dynex.py
    ├── test_acm.py

```
---


## 🛡️ Detected Attack Categories
CATOR detects **volumetric**, **application-layer**, and **multi-vector** DDoS attacks, including:

- **Volumetric Floods**: SYN, UDP, ICMP floods, amplification
- **Application-Layer Attacks**: Slow HTTP, DNS query floods
- **Multi-Vector Campaigns**: Concurrent volumetric + application attacks
- **Variable-Intensity Sequences**: Gradual escalation or alternating traffic rates
- **Control-Plane Saturation**: SDN controller flow-setup floods
- **Stealth/Evasive Threats**: Low-rate floods, spoofed traffic, coordinated botnets

---

## 📊 Utilized Datasets

CATOR is evaluated using **five benchmark IoT and IIoT security datasets**:

1. **[CICIoT2023](https://www.unb.ca/cic/datasets/iotdataset-2023.html)**  
   - 107 types of IoT attacks, including DDoS, DoS, data exfiltration, etc.  
   - Features: statistical, flow-based, time-based metrics  

2. **[ToN-IoT](https://research.unsw.edu.au/projects/toniot-datasets)**  
   - Real-world IoT telemetry data from smart home and industrial environments  
   - Contains benign and malicious flows  

3. **[IoT-ID20](https://www.kaggle.com/datasets/rohulaminlabid/iot-id20)**  
   - Network traces from various IoT devices under normal and attack scenarios  

4. **[UNSW-NB15](https://research.unsw.edu.au/projects/unsw-nb15-dataset)**  
   - Network intrusion dataset with modern attack categories, suitable for training network defense models  

5. **[Edge-IIoTset](https://www.kaggle.com/datasets/iotnet/edgeiiotset)**  
   - Industrial IoT dataset covering various attack types against edge computing environments  

**Preprocessing** is handled via `datasets/preprocessing.py` and paths are set in `config/datasets_config.json`.

---

## ⚙️ Installation

### Requirements
- Python 3.8+
- P4C (p4c-bm2-ss)
- BMv2 (simple_switch_grpc)
- Mininet / Mininet-WiFi
- Ryu SDN framework
- Flask

### Setup
```bash
git clone https://github.com/SD-IoT-AE/CATOR.git
cd CATOR
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🛠 Configuration

All configurations are stored in `config/`:

- `cator_config.json` – Global thresholds, parameters
- `datasets_config.json` – Dataset paths and preprocessing options
- `p4_switch_config.json` – Switch IDs, ports, feature extraction mapping
- `controller_config.json` – Multi-controller topology parameters
- `mitigation_policies.json` – Rate-limit/drop rules for ACM

---

## 🏋️ Training

To train the DYNEX ensemble classifier:
```bash
python training/train_dynex.py 
```

---

## 📊 Evaluation

To evaluate the trained model:
```bash
python training/eval_dynex.py 
```

---

## 📈 Results Summary

### **1️⃣ Binary Classification (Across Datasets)**

| Dataset     | Model    | DA (%) | PR (%) | SN (%) | F1-S (%) | TPR (%) | NPV (%) | MCC  | AUC  | FPR (%) | FNR (%) | EDR (%) | ATRT (s) |
|-------------|----------|--------|--------|--------|----------|---------|---------|------|------|---------|---------|---------|----------|
| CICIoT2023  | DYNEX    | 98.75  | 98.22  | 98.94  | 98.59    | 98.91   | 97.95   | 0.97 | 0.99 | 1.05    | 0.93    | 1.68    | 1.12     |
| ToN-IoT     | DYNEX    | 97.34  | 97.12  | 97.43  | 97.26    | 97.39   | 97.01   | 0.96 | 0.98 | 1.26    | 1.13    | 1.74    | 1.28     |
| IoT-ID20    | DYNEX    | 95.68  | 95.03  | 95.46  | 95.26    | 95.46   | 94.91   | 0.94 | 0.96 | 2.08    | 1.94    | 2.12    | 1.41     |
| UNSW-NB15   | DYNEX    | 94.53  | 94.06  | 94.58  | 94.34    | 94.58   | 93.92   | 0.93 | 0.95 | 2.70    | 2.51    | 2.34    | 1.54     |
| Edge-IIoTset| DYNEX    | 93.05  | 92.34  | 93.20  | 92.80    | 93.20   | 92.20   | 0.91 | 0.94 | 3.22    | 3.06    | 2.75    | 1.71     |

*Only DYNEX results shown for brevity; full table with LightGBM, XGBoost, GRBoost, and EXTree available in the paper.*

---

### **2️⃣ Multi-Class Classification (CICIoT2023)**
- **Accuracy**: 97.82%
- **F1-Score**: 97.55%
- **Low false positive rate**: ~2.1%
- Successfully distinguishes **specific attack types** (e.g., HTTP Flood, SYN Flood, SlowLoris, DNS Amplification)

---

### **3️⃣ Multi-Scenario / Emulated Attacks**
**10 attack scenarios** tested (1–12 Gbps, sequential, multi-vector, persistent, hybrid).
- Avg. detection accuracy: **96.91%**
- Avg. false positives: **2.03%**
- Packet loss reduced by **50–70%**
- Latency restored to **<200 ms** in **3–10 s**
- Example:  
  *Complex Multi-Vector Attack (12 Gbps)* → reduced packet loss from **50%+** to **20%**, latency from **800 ms** to **250 ms**.

---

### **4️⃣ Multi-Controller Mitigation Performance**
- **Mitigation latency** improved by **42%** vs. single-controller
- **Detection coverage** sustained at **98.3%** during failover
- **Service disruption** under **1.5 s** in failover tests

---

## 🖥 Emulated Deployment

1. **Start controllers:**
```bash
bash deployment/start_controllers.sh
```
2. **Deploy P4 programs:**
```bash
bash deployment/deploy_p4_switches.sh
```
3. **Run Mininet topology:**
```bash
sudo python deployment/mininet_topology.py
```

---

## 🌍 Real-World Deployment

1. Compile P4 for target hardware (Intel Tofino, NetFPGA, etc.)
2. Update `p4_switch_config.json` with real ports and device IDs
3. Connect controllers to production network
4. Start ACM and AWTA Python processes
5. Verify gRPC connectivity

---

## 🛠 Troubleshooting

- **Switch not connecting:** Check gRPC port in `p4_switch_config.json`
- **Low accuracy:** Retrain with more balanced dataset
- **Controller timeout:** Verify firewall and REST API ports

---
