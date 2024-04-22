import logging
import os
import shutil
import traceback

from starlette.responses import JSONResponse

from config import APP, POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, PATH_TO_UPLOAD

from fastapi import FastAPI, UploadFile, File

from utility import unzip
from utility_postgres import shapeFile2Postgis, load_dbf, load_shapefile

app = FastAPI(summary= "Applicativo per la gestione di file shape",
              description="""
        """,
              version= "0.0.1")

logger = logging.getLogger(APP)

@app.get("/upload_zip")
async def upload_zip(validation_id:int,file: UploadFile = File(...)):
    try:
        file_path=os.path.join(PATH_TO_UPLOAD,str(file.filename))
        # Sposta il file nella cartella di destinazione
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        #unzip file
        shapefile_folder=unzip(file_path,PATH_TO_UPLOAD)
        os.remove(file_path)
        map_file={"data":[],"validation_id":validation_id}
        for file in os.listdir(shapefile_folder):
            if file.endswith('.dbf'):
                table_name=file.split(".")[0]
                map_create, columns, _, columns_list=load_dbf(file,table_name,group_id=None,srid_validation=None)
                map_temp={table_name:map_create}
                map_file["data"].append(map_temp)
            if file.endswith('.shp'):
                table_name=file.split(".")[0]
                res, columns, gdf, columns_list, start_time, elapsed,map_create=load_shapefile(file,table_name,group_id=None,srid_validation=None)
                if res:
                    map_temp={table_name:map_create}
                    map_file["data"].append(map_temp)
        return JSONResponse(content=map_file, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/shape_file2postgis")
async def shape_file2postgis(file_zip:str, schema:str=None):
    conn_str_db = f"host='{POSTGRES_SERVER}' port='{POSTGRES_PORT}' dbname='{POSTGRES_DB}' user='{POSTGRES_USER}' password='{POSTGRES_PASSWORD}'"
    try:
        result=shapeFile2Postgis(file_zip,conn_str_db,schema)
        return JSONResponse(content={"result": result,"esito":"OK"}, status_code=201)
    except Exception as e:
        logger.error(f"Error:{e}", stack_info=True)
        print(f"Error:{e}")
        traceback.print_exc()
        return JSONResponse(content={"esito":"KO","error": str(e)}, status_code=501)
