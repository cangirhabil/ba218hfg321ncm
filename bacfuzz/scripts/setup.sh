# !/bin/bash

cd ../
python get-pip.py
python -m venv venv
source venv
pip install -r requirements.txt
pip install pytest-playwright
playwright install
playwright install-deps --dry-run
