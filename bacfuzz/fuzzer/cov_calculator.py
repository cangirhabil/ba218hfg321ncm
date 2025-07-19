import csv
import os
from datetime import datetime
from os.path import join, isfile

from config import config
from general_functions import read_cov_from_file

def calculate_coverage(start_time=datetime.now()):
    for f in os.listdir(config.data['COV_PATHS']):
        filename = join(config.data['COV_PATHS'], f)
        if isfile(filename):
            print(f"[COVCALCULATOR] Calculating coverage from ", filename)
            try:
                read_cov_from_file(filename)
            except Exception as e:
                print(e)

            print(f"[COVCALCULATOR] Deleting the file {filename} after getting the coverage")
            try:
                os.system(f"rm {filename}")
            except Exception as e:
                print(e)

    foldername="default"
    if "PROJECT_NAME" in config.data:
        foldername = config.data["PROJECT_NAME"]
    dir_location = os.path.join(os.getcwd(), '../attack_surface', foldername)
    if not os.path.exists(dir_location):
        os.makedirs(dir_location, exist_ok=True)

    filename = f"coverage-{start_time.timestamp()}.csv"
    with open(f"{dir_location}/{filename}", "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow([datetime.now().timestamp(), len(config.line_coverage)])

if __name__ == "__main__":
    config.load_config(file_path="../configs/config-general.yaml")
    calculate_coverage()