# Artefact for "BACFuzz: Revealing Broken Access Control on Web Applications with LLM, Grey-box Fuzzing, and SQL Checking"

## What is This?
This repository contains the artefact accompanying our paper submission. It includes:

- Source code
- Web Under Test
- Scripts to reproduce our experiments
- Documentation for setup and usage

## Repository Structure

- /bacfuzz/ # Source code
- /bacfuzz/scripts # Scripts to run the experiments
- /bacfuzz/final_results/ # Final output from experiments
- /WUT # Web Under Test
- README.md # This file

## Getting Started

### Requirements

- Python 3.10+
- pip, virtualenv, or conda
- (List any other dependencies like PyTorch, Docker, etc.)

### Setup Instructions
- Open directory /bacfuzz/scripts in a terminal
- Run ./setup.sh to install required libraries
- Start Docker (e.g., by running 'systemctl start docker')
- Configure an experiment you want to run. For example, open and edit fuzzer-CVE_2025_0802.sh
- To run the experiment, run ./fuzzer-CVE_2025_0802.sh
- The experiment will run the web under test in a Docker container. After the web is ready, BACFuzz is launched for several hours (depending on how long you set up the time)

