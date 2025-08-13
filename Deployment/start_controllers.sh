#!/bin/bash


echo "[Deployment] Starting Central Controller (C0)..."

ryu-manager controllers/central_controller.py --observe-links &



echo "[Deployment] Starting Domain Controller (C1)..."

python3 controllers/domain_controller.py --port 6654 &



echo "[Deployment] Starting Domain Controller (C2)..."

python3 controllers/domain_controller.py --port 6655 &



echo "[Deployment] All controllers started."
