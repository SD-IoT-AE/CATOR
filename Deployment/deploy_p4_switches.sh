#!/bin/bash


set -e



P4C_BM2="p4c-bm2-ss"



echo "[Deployment] Compiling AWTA P4 program..."

$P4C_BM2 p4/awta.p4 -o p4/awta.json



echo "[Deployment] Compiling FCSTD P4 program..."

$P4C_BM2 p4/fcstd.p4 -o p4/fcstd.json



echo "[Deployment] Compiling Feature Extraction P4 program..."

$P4C_BM2 p4/features_extraction.p4 -o p4/features_extraction.json



echo "[Deployment] Starting BMv2 switches..."

# Example: Starting one switch with AWTA


simple_switch_grpc --device-id 0 --no-p4 --log-console p4/awta.json -- --grpc-server-addr 127.0.0.1:50051 &
