import os
DB_FILE_LOCATION = "/mnt/hgfs/to_share/stars_csv/cleaned_stars.tsv"
# DB_FILE_LOCATION = "/mnt/hgfs/to_share/stars_csv/337.all.tsv"
DB_SEPARATOR = "\t"

RA_COLUMN_INDEX = 0
DEC_COLUMN_INDEX = 1
ID_COLUMN_INDEX = 7
BRIGHTNESS_COLUMN_INDEX = 22

RESULTS_DIR = "results"

os.makedirs(RESULTS_DIR, exist_ok=True)
