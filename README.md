# Artefact for "BACFuzz: Exposing the Silence on Broken Access Control Vulnerabilities in Web Applications"

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

### Setup Instructions
- Open directory /bacfuzz/scripts in a terminal
- Run ./setup.sh to install required libraries
- Start Docker (e.g., by running '
  ```
  systemctl start docker
  ```

- Since BACFuzz uses DeepSeek API, you should export your API KEY to Environment Variable
  ```
  export DEEPSEEK_API_KEY=<<YOUR_API_KEY>>
  ```
- Configure an experiment you want to run. For example, open and edit fuzzer-CVE_2025_0802.sh
- To run the experiment, run ./fuzzer-CVE_2025_0802.sh
- The experiment will run the web under test in a Docker container. After the web is ready, BACFuzz is launched for several hours (depending on how long you set up the time)
  - The MainDriver starts first to crawl the web under test. HTTP requests catched during crawling are stored in attack_surface folder.
  - After the MainDriver finishes, the ActiveChecker starts to fuzz the web under test.
  - The final result of BAC detected is stored in final_result folder
