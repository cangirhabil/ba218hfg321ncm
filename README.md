# Artefact for "BACFuzz: Exposing the Silence on Broken Access Control Vulnerabilities in Web Applications"

## What is This?
This repository contains the artefact accompanying our paper submission. It includes:

- BACFuzz source code
- Web Under Test (WUT)
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

- Python 3
- Docker

### Setup Instructions
- Open directory /bacfuzz/scripts in a terminal
- Run ./setup.sh to install required libraries
- Start Docker
  ```
  systemctl start docker
  ```

- Since BACFuzz uses DeepSeek API, you should export your API KEY to Environment Variable
  ```
  export DEEPSEEK_API_KEY=<<YOUR_API_KEY>>
  ```
- Configure an experiment you want to run. For example, open and edit fuzzer-CVE_2025_0802.sh
- To run the experiment, run ./fuzzer-CVE_2025_0802.sh
- The experiment runs the target web application inside a Docker container. Once the web application is ready, BACFuzz is launched and runs for several hours (depending on the configured duration).
  - The MainDriver starts first and crawls the target web application. During crawling, all captured HTTP requests are stored in the attack_surface folder.
  - After the MainDriver finishes, the ActiveChecker begins fuzzing the target web application.
  - The final results, including any detected BAC vulnerabilities, are saved in the final_result folder
