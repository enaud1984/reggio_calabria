from collections import namedtuple
import json
import logging
import os
import re
import shutil
import subprocess
import traceback
from datetime import datetime

from starlette.responses import JSONResponse

from DAO import CodeInput, ColumnResponse, MapTables
from config import APP, LIST_LANG, LIST_LOAD, POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, PATH_TO_UPLOAD, \
    LIST_SRID, async_session_Db

from fastapi import FastAPI, UploadFile, File, Query

from importerLayers import delete_layers, publish_layers
from richieste_dal import RichiesteUpload, RichiesteLoad, RichiesteModel, RichiesteExecution
from utility import unzip, get_md5
from utility_R import invoke_R
from utility_postgres import shapeFile2Postgis, load_dbf, load_shapefile,get_map_files
import pandas as pd
import geopandas as gd


app = FastAPI(summary= "Applicativo per la gestione di file shape",
              description="""
        """,
              version= "0.0.1")

logger = logging.getLogger(APP)

@app.put("/upload_zip")
async def upload_zip_file(group_id:str, file_zip: UploadFile = File(...)):
    try:
        file_path_zip=os.path.join(PATH_TO_UPLOAD,str(file_zip.filename))
        # Sposta il file nella cartella di destinazione
        with open(file_path_zip, "wb") as buffer:
            shutil.copyfileobj(file_zip.file, buffer)
        #unzip file
        shapefile_folder=unzip(file_path_zip,PATH_TO_UPLOAD)
        logger.info("Uploading shapefile and unzip")
        mapping_fields = MapTables(data=[])
        list_files_dbf=[]
        list_files_shp=[]
        map_results={}
        for root, dirs, files in os.walk(shapefile_folder):
            for file in files:
                file_path=os.path.join(root, file)
                if file.endswith('.dbf'):
                    list_files_dbf.append([file_path,file])
                    table_name=file.split(".")[0]
                if file.endswith('.shp'):
                    list_files_shp.append([file_path,file])
        list_table_shp=[file[:-4] for file_path,file in list_files_dbf] 
        list_create =[]
        list_files_dbf =[(file_path,file) for file_path,file in list_files_dbf if file[:-4] not in list_table_shp]   

        for file_path,file in list_files_dbf:
            table_name = file[:-4]
            if table_name not in list_table_shp:
                map_create, columns, _, columns_list,df,elapsed = load_dbf(file_path, table_name,group_id,None)
                info={
                    "columns":columns,
                    "file":file_path,
                    "table_name":table_name, 
                    "columns_list":columns_list, 
                    "elapsed":elapsed,
                    "map_create":map_create
                }
                map_results[table_name]=info
                list_create.append([None,map_create,namedtuple("Info",list(info.keys()))(**info)])
        for file_path,file in list_files_shp:
            table_name = file[:-4]
            if table_name in list_table_shp:
                res, columns, gdf, columns_list, start_time, elapsed,map_create = load_shapefile(file_path,table_name,group_id,None)
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
                map_results[table_name]=info
                list_create.append([srid,map_create,namedtuple("Info",list(info.keys()))(**info)])
        for srid,map_create,info in list_create:
            for col, tipo in map_create.items():
                column_response = ColumnResponse(
                    filename=info.file,
                    table=info.table_name,
                    column=col,
                    tipo=tipo,
                    srid=srid,
                    column_name=col,
                    importing=True
                )
                mapping_fields.data.append(column_response)
        list_files=[file_path for file_path,file in list_files_dbf+list_files_shp]
        async with async_session_Db() as sessionpg:
            async with sessionpg.begin():
                request_dal = RichiesteUpload(sessionpg)
                md5_zip=get_md5(file_zip.filename)
                os.remove(file_path_zip)
                res_PostGres = await request_dal.create_request(ID_SHAPE=None,
                                                                SHAPEFILE=file_zip.filename,
                                                                DATE_UPLOAD=datetime.now(),
                                                                STATUS="UPLOAD ZIP",
                                                                GROUP_ID=group_id,
                                                                SRID=None,
                                                                PATH_SHAPEFILE=shapefile_folder,
                                                                MD5=md5_zip,
                                                                USERFILE=list_files,
                                                                RESPONSE=mapping_fields.to_dict())

                logger.info(f"OK WRITE ON SINFIDB, VALIDATION_ID: {res_PostGres.ID_SHAPE}")
        resp= json.loads(mapping_fields.model_dump_json())
        return JSONResponse(content=resp, status_code=200)
    except Exception as e:
        logger.error(f"Error:{e}", stack_info=True)
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/load_shapefile2postgis")
async def load_shapefile2postgis(validation_id: int,
                                 group_id: str,
                                 schema: str = "public",
                                 srid_validation=Query(description="Selezionare SRID di riferimento",enum=["auto"]+LIST_SRID),
                                 load_type=Query(description="Selezionare modalita caicamento tabella",enum=LIST_LOAD),
                                 mapping_fields: MapTables = None):
    try:
        logger.info("Load Shape files to PostGis...")
        async with async_session_Db() as sessionpg:
            async with sessionpg.begin():
                request_dal = RichiesteLoad(sessionpg)
                res_PostGres = await request_dal.create_request(ID_SHAPE=None,
                                                                DATE_LOAD=datetime.now(),
                                                                STATUS="LOAD SHAPEFILE",
                                                                GROUP_ID=group_id,
                                                                REQUEST=mapping_fields.to_dict())

        #host='127.0.0.1' port='5444' dbname='postgres' user='postgres' password='postgres'
        conn_str_db: str = f"host='{POSTGRES_SERVER}' port='{POSTGRES_PORT}' dbname='{POSTGRES_DB}' user='{POSTGRES_USER}' password='{POSTGRES_PASSWORD}'"
                            
        map_files = get_map_files(validation_id,conn_str_db)
        if srid_validation=="auto":
            srid_validation = None
        result = shapeFile2Postgis(validation_id,map_files,mapping_fields,group_id,conn_str_db,schema=schema,
                                 srid=srid_validation,load_type=load_type)
        #TODO: inserire result in db con update in modo da poterlo usare dopo?
        return JSONResponse(content={"result": result,"esito":"OK","layers":result}, status_code=201)
    except Exception as e:
        logger.error(f"Error:{e}", stack_info=True)
        print(f"Error:{e}")
        traceback.print_exc()
        return JSONResponse(content={"esito":"KO","error": str(e)}, status_code=501)


@app.get("/get_all_upload")
async def get_all_upload(id_shape:int=None,group_id=None,skip: int = 0, limit: int = 100) :
    '''_Summary_<br>
        _Lista delle richieste storiche<br>

    __Args:__<br>
        <li>id_shape (StateProcess): __id__ della richiesta  che effettua il caricamento_. Defaults to Null. </li>
        <li>group_id (id, optional): __group_id__ della richiesta  che effettua il caricamento_. Defaults to Null.</li>
        <li>__skip__ (int, optional): _parametro della paginazione per saltare le righe_. Defaults to 0.</li>
        <li>__limit__ (int, optional): _parametro di paginazione per avere un limite sul numero di record restituiti _. Defaults to 100.</li>

    __Returns:__<br>
        _type_: _json_
        lista delle richieste al director o del worker
    '''

    try:
        async with async_session_Db() as session:
            async with session.begin():
                request_dal = RichiesteUpload(session)
                ret = await request_dal.get_all_requests(id_shape, group_id, skip, limit)
        return ret
    except Exception as e:
        logger.error(f"Error:{e}", stack_info=True)
        return JSONResponse(content={"error": str(e),"group_id":group_id,
                                     "id":id_shape
                                     },
                            status_code=501)

@app.get("/get_all_shapes")
async def get_all_shapes(id_shape:int=None,group_id=None,skip: int = 0, limit: int = 100) :
    '''_Summary_<br>
        _Lista delle richieste storiche<br>

    __Args:__<br>
        <li>__id_shape__ (StateProcess): _id shape__ </li>
        <li>__group_id_ (id, optional): __group_id__ della richiesta  che effettua il caricamento_. Defaults to Null.</li>
        <li>__skip__ (int, optional): _parametro della paginazione per saltare le righe_. Defaults to 0.</li>
        <li>__limit__ (int, optional): _parametro di paginazione per avere un limite sul numero di record restituiti _. Defaults to 100.</li>

    __Returns:__<br>
        _type_: _json_
        lista delle richieste al director o del worker
    '''

    try:
        async with async_session_Db() as session:
            async with session.begin():
                request_dal = RichiesteLoad(session)
                ret = await request_dal.get_all_requests(id_shape, group_id, skip, limit)
        return ret
    except Exception as e:
        logger.error(f"Error:{e}", stack_info=True)
        return JSONResponse(content={"error": str(e),"group_id":group_id,
                                     "id":id_shape
                                     },
                            status_code=501)
@app.delete("/delete_shape")
async def delete_shape(ID_SHAPE: int,group_id):
    """_summary_<br>
                cancellazione funzione<br>
         __Args:__<br>
             <li> function_name (str): _funzione da cancellare_ </li>

        __Returns__:<br>
            _type_: _json_

        """
    try:
        async with async_session_Db() as session:
            async with session.begin():
                request_dal = RichiesteLoad(session)
                ret = await request_dal.get_request(ID_SHAPE=ID_SHAPE)
                #cancellazione folder da to_upload
                shutil.rmtree(ret.PATH_SHAPEFILE)
                #cancellazione layer pubblicati
                delete_layers(group_id,[l.split(".")[0] for l in ret.USERFILE])
                return await request_dal.del_request(ID_SHAPE=ID_SHAPE)
    except Exception as e:
        logger.error(f"Error:{e}", stack_info=True)
        return JSONResponse(content={"error": str(e),"group_id":group_id,
                                     "id":ID_SHAPE
                                     },
                            status_code=501)

#TODO: servizio per update shape sul db
#TODO: servizio per caricare il python del modello sul db  tabella


@app.post("/upload_lib")
async def upload_lib(group_id, file_zip: UploadFile = File(...)):
    pass

@app.post("/upload_model")
async def upload_model(group_id, code_str: str):
    try:
        ID_MODEL=None
        async with async_session_Db() as session:
            async with session.begin():
                request_dal = RichiesteModel(session)
                res = await request_dal.create_request(ID_MODEL=None,
                                                       DATE_MODEL=datetime.now(),
                                                       STATUS="LOAD MODEL",
                                                       GROUP_ID=group_id,
                                                       CODE=code_str,
                                                       PARAMS=None, #risposta di una load precedente per ID_SHAPE? ci vuole?
                                                       LIBRARY=False)
                ID_MODEL = res.ID_MODEL
    except Exception as e:
        logger.error(f"Error:{e}", stack_info=True)
        return JSONResponse(content={"error": str(e),"group_id":group_id,
                                     "id":ID_MODEL
                                     },
                            status_code=501)


@app.post("/execute_code/")
async def execute_code(group_id:str, shape_id: int, params: dict, mapping_output: dict,
                       language: str = Query(description="Selezionare linguaggio",enum=LIST_LANG),
                       model_id_or_code: str = Query(description="Selezionare la sorgente del codice",enum=["Model_id","Testo"]),
                       model_id_code=None):

    from config import engine_Db_no_async,CHUNCKSIZE,connection_string
    logger.info("Esecuzione del modello")
    async with async_session_Db() as session:
        async with session.begin():
            request_dal = RichiesteExecution(session)

            res = await request_dal.create_request(ID_EXECUTION=None,
                                                   DATE_EXECUTION=datetime.now(),
                                                   STATUS="Execution MODEL",
                                                   GROUP_ID=group_id,
                                                   FK_MODEL=model_id_code if model_id_or_code == "Model_id" else None,
                                                   FK_SHAPE=shape_id,
                                                   PARAMS=params,
                                                   MAPPING_OUTPUT=mapping_output,
                                                   RESULTS=None)
            id_execution=res.ID_EXECUTION
    code=None
    results=None
    layers=None
    if model_id_or_code == "Testo":
        code = model_id_code
    elif model_id_or_code == "Model_id":
        code="" #query sul db

    # Analisi del codice alla ricerca dei parametri %param1%
    params = re.findall(r'%([^%]+)%', code)
    logger.info(f"Parametri trovati nel codice: {params}")
    # Sostituzione dei parametri con i valori forniti dall'utente
    for param in params:
        value = params[param]
        code = code.replace(f'%{param}%', value)
    engine = engine_Db_no_async
    # Esecuzione del codice
    if language == "python":
        try:
            variables = {}
            global_df = {}
            mapping_shape = {} #prendere i nomi delle tabelle e il tipo dal db
            for tablename,type_dataframe in mapping_shape.items():
                if type_dataframe=="gd.GeoDataFrame":
                    gdf: gd.GeoDataFrame = gd.read_postgis(f"{group_id}.{tablename}",connection_string)
                    global_df[tablename] = gdf
                if type_dataframe=="pd.DataFrame":
                    df:pd.DataFrame = pd.read_sql_table(f"{group_id}.{tablename}",connection_string)
                    global_df[tablename] = df
                
            exec(code, global_df, variables)
            layers = []
            tables = []    
            for k,v in mapping_output.items():
                df_result = None
                table_name = v
                #df_out=cercare su code_input.data il nome della variabile con df_out = True
                df_result = variables[k]
                if hasattr(df_result, "crs"):
                    gdf:gd.GeoDataFrame = df_result
                    gdf.to_postgis(table_name, engine, if_exists='replace', index=False, schema=group_id,chunksize=CHUNCKSIZE)
                    layers.append(table_name)
                elif type(df_result) == pd.DataFrame:
                    df:pd.DataFrame=df_result
                    df.to_sql(table_name, engine, if_exists='replace', index=False, schema=group_id,chunksize=CHUNCKSIZE)
                    tables.append(table_name)
            #TODO:pubblicazione su geoserver
            layers = publish_layers(group_id,layers)

        except Exception as e:
            return JSONResponse(status_code=500, content=f"Errore durante l'esecuzione dello script Python {e}")
    elif language == "r":
        try:
            result,variables=invoke_R(code)
            layers = []
            tables = []
            for k,v in mapping_output.items():
                df_result = None
                table_name = v
                #df_out=cercare su code_input.data il nome della variabile con df_out = True
                df_result = variables[k]
                if hasattr(df_result,"crs"):
                    gdf:gd.GeoDataFrame = df_result
                    gdf.to_postgis(table_name, engine, if_exists='replace', index=False, schema=group_id,chunksize=CHUNCKSIZE)
                    layers.append(table_name)
                elif type(df_result)==pd.DataFrame:
                    df:pd.DataFrame=df_result
                    df.to_sql(table_name, engine, if_exists='replace', index=False, schema=group_id,chunksize=CHUNCKSIZE)
                    tables.append(table_name)
            #TODO:pubblicazione su geoserver
            layers = publish_layers(group_id,layers)
            results={}
            #return JSONResponse(status_code=200, content={"result": result})
        except Exception as e:
            return JSONResponse(status_code=500, content=f"Errore durante l'esecuzione dello script Python {e}")

    async with async_session_Db() as session:
        async with session.begin():
            res = RichiesteExecution(session)
            res = await request_dal.update_request(ID_EXECUTION=id_execution,
                                                   RESULTS=results)
    return JSONResponse(status_code=200, content={"layers": layers,"results":results})
