import logging
import zipfile
from datetime import datetime
import os
from multiprocessing.pool import ThreadPool

import psycopg2

from config import ENABLE_POOL_LOAD, APP, engine_sinfiDb_no_async, CHUNCKSIZE

logger = logging.getLogger(APP)

def unzip(path_to_zip_file,directory_to_extract_to):
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_contents = zip_ref.namelist()
        folder_name = os.path.dirname(zip_contents[0])
        zip_ref.extractall(directory_to_extract_to)
    logger.info(f"Unzipped {path_to_zip_file} to {directory_to_extract_to}")
    return os.path.join(directory_to_extract_to, folder_name)

def get_map_files(shapefile_folder):
    map_files={}
    list_files =sorted(os.listdir(shapefile_folder),reverse=False)
    for file_name in list_files:
        k = file_name[:-4].lower()
        if k not in map_files or file_name.endswith('.shp'):
            if file_name.endswith('.shp'):
                map_files[k] = file_name
            elif file_name.endswith('.dbf') :
                map_files[k] = file_name

def find_specTable(map_tables,key):
    for item in map_tables["data"]:
        if key in item:
            return item[key]

def change_column_types(df, json_types):
    for colonna, tipo in json_types.items():
        df[colonna] = df[colonna].astype(tipo)
    return df