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