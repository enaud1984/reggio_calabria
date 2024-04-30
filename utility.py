from collections import namedtuple
import hashlib
import logging
import zipfile
from datetime import datetime
import os
from multiprocessing.pool import ThreadPool

import psycopg2

from config import ENABLE_POOL_LOAD, APP, engine_Db_no_async, CHUNCKSIZE

logger = logging.getLogger(APP)

def unzip(path_to_zip_file,directory_to_extract_to):
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_contents = zip_ref.namelist()
        folder_name = os.path.dirname(zip_contents[0])
        zip_ref.extractall(directory_to_extract_to)
    logger.info(f"Unzipped {path_to_zip_file} to {directory_to_extract_to}")
    return os.path.join(directory_to_extract_to, folder_name)


def analyze_file(file,file_path,group_id,load_func,is_shape=False,srid=None):
    table_name = file[:-4]
    if is_shape:
        res, columns, gdf, columns_list, start_time, elapsed,map_create = load_func(file_path,table_name,group_id,None)
        srid  = gdf.crs.to_epsg()
        info ={
                "file":file_path,
                "table_name":table_name, 
                "columns":columns, 
                "columns_list":columns_list, 
                "elapsed":elapsed,
                "srid":srid,
                "map_create":map_create
        }
    else:
        map_create, columns, _, columns_list,df,elapsed = load_func(file_path, table_name,group_id,srid)
        info={
            "columns":columns,
            "file":file_path,
            "table_name":table_name, 
            "columns_list":columns_list, 
            "elapsed":elapsed,
            "map_create":map_create
        }
    info = namedtuple("Info",list(info.keys()))(**info)
    return table_name,map_create,info


def find_specTable(map_tables,key):
    map_field ={}
    for item in map_tables.data:
        if key==item.table:
            map_field[item.column_name]=item
    return map_field

def change_column_types(df, json_types):
    postgis_types_mapping = {
        'str': 'text',
        'object': 'text',
        'int64': 'integer',
        'float64': 'double precision',
        'float32': 'double precision',
        'int32': 'integer',
        'int16': 'integer',
    }
    for colonna, field in json_types.items():
        tt =type(df[colonna][0]).__name__
        dftype=postgis_types_mapping.get(tt)
        if dftype is not None and field.tipo!=dftype:
            df[colonna] = df[colonna].astype(dftype)
    return df

def get_md5(fname,path="to_upload"):
    if fname.endswith(".zip"):
        path_to_unzip_file = os.path.join(path, fname)
        return get_md5_file(path_to_unzip_file)
    else:
        #to_upload\Shape_flat20240205_1439\Shape_flat
        f_list=fname.split("\\")
        nome_path_zip=os.path.join("uploaded_zip",f"{f_list[-2]}.zip")
        path_da_zippare=os.path.join(*f_list[:-1])
        zipp(path_da_zippare,nome_path_zip)
        md5= get_md5(nome_path_zip.split("\\")[-1])
        os.remove(nome_path_zip)
        return md5

def get_md5_file(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def zipp(folder_path,zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))