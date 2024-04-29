import logging
import os
import re
import shutil
import subprocess
import traceback
from datetime import datetime

from starlette.responses import JSONResponse

from DAO import CodeInput, ColumnResponse, MapTables
from config import APP, LIST_LANG, POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, PATH_TO_UPLOAD, \
    LIST_SRID, async_session_Db

from fastapi import FastAPI, UploadFile, File, Query

from importerLayers import delete_layers, publish_layers
from richieste_dal import RichiesteDAL
from utility import unzip, get_map_files, get_md5
from utility_R import invoke_R
from utility_postgres import shapeFile2Postgis, load_dbf, load_shapefile
import pandas as pd
import geopandas as gd


app = FastAPI(summary= "Applicativo per la gestione di file shape",
              description="""
        """,
              version= "0.0.1")

logger = logging.getLogger(APP)

@app.put("/upload_zip")
async def upload_zip_file(group_id:str,srid:int=Query(description="Selezionare SRID di riferimento", enum=LIST_SRID), file_zip: UploadFile = File(...)):
    try:
        file_path_zip=os.path.join(PATH_TO_UPLOAD,str(file_zip.filename))
        # Sposta il file nella cartella di destinazione
        with open(file_path_zip, "wb") as buffer:
            shutil.copyfileobj(file_zip.file, buffer)
        #unzip file
        shapefile_folder=unzip(file_path_zip,PATH_TO_UPLOAD)
        mapping_fields = MapTables(data=[])
        list_files_dbf=[]
        list_files_shp=[]
        map_results={}
        for root, dirs, files in os.walk(shapefile_folder):
            for file in files:
                file_path=os.path.join(root, file)
                if file.endswith('.dbf'):
                    list_files_dbf.append(file_path,file)
                    table_name=file.split(".")[0]
                if file.endswith('.shp'):
                    list_files_shp.append(file_path,file)
        list_table_shp=[file[:-4] for file_path,file in list_files_dbf] 
        list_create =[]
        list_files_dbf =[(file_path,file) for file_path,file in list_files_dbf if file[1][:-4] not in list_table_shp]   
        for file_path,file in list_files_dbf:
            table_name = file[:-4]
            if table_name not in list_table_shp:
                map_create, columns, _, columns_list,df = load_dbf(file_path, table_name,group_id,srid)
                map_results[table_name]={
                    "result":res,
                    "columns":columns, 
                    "columns_list":columns_list, 
                    "elapsed":elapsed,
                    "map_create":map_create
                }
                list_create.append(map_create)
        for file_path,file in list_files_shp:
            table_name = file[:-4]
            if table_name not in list_table_shp:
                res, columns, gdf, columns_list, start_time, elapsed,map_create = load_shapefile(file_path,table_name,group_id,srid)
                map_results[table_name]={
                    "result":res,
                    "columns":columns, 
                    "columns_list":columns_list, 
                    "elapsed":elapsed,
                    "map_create":map_create
                }
        for map_create in map_create:
            list_create.append(map_create)        
            for col, tipo in map_create.items():
                column_response = ColumnResponse(
                    filename=file,
                    table=table_name,
                    column=col,
                    tipo=tipo,
                    column_name=col,
                    importing=True
                )
                mapping_fields.data.append(column_response)
        list_files=list(map_create.keys())
        async with async_session_Db() as sessionpg:
            async with sessionpg.begin():
                request_dal = RichiesteDAL(sessionpg)
                md5_zip=get_md5(file_zip.filename)
                os.remove(file_path_zip)
                res_PostGres = await request_dal.create_request(ID_SHAPE=None,
                                                                SHAPEFILE=file_zip.filename,
                                                                DATE_UPLOAD=datetime.now(),
                                                                STATUS="UPLOAD ZIP",
                                                                GROUP_ID=group_id,
                                                                SRID=srid,
                                                                PATH_SHAPEFILE=shapefile_folder,
                                                                MD5=md5_zip,
                                                                USERFILE=list_files,
                                                                RESPONSE=mapping_fields.to_dict())

                logger.info(f"OK WRITE ON SINFIDB, VALIDATION_ID: {res_PostGres.ID_SHAPE}")

        return JSONResponse(content=str(mapping_fields.model_dump_json()), status_code=200)
    except Exception as e:
        logger.error(f"Error:{e}", stack_info=True)
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/load_shapefile2postgis")
async def shape_file2postgis(validation_id: int,
                             shapefile_folder: str,
                             group_id: None,
                             conn_str_db: str = f"host='{POSTGRES_SERVER}' port='{POSTGRES_PORT}' dbname='{POSTGRES_DB}' user='{POSTGRES_USER}' password='{POSTGRES_PASSWORD}'",
                             schema: str = None,
                             srid_validation=Query(description="Selezionare SRID di riferimento",enum=LIST_SRID),
                             load_type="append",
                             mapping_fields: MapTables = None):
    try:
        #TODO:Update request
        map_files=get_map_files(shapefile_folder)
        result = shapeFile2Postgis(validation_id,map_files,shapefile_folder,mapping_fields,group_id,conn_str_db,schema=schema,
                                 srid=srid_validation,load_type=load_type)
        layers = publish_layers(group_id,layers)
        return JSONResponse(content={"result": result,"esito":"OK","layers":layers}, status_code=201)
    except Exception as e:
        logger.error(f"Error:{e}", stack_info=True)
        print(f"Error:{e}")
        traceback.print_exc()
        return JSONResponse(content={"esito":"KO","error": str(e)}, status_code=501)


@app.get("/requests")
async def get_all_requests(id:int=None,group_id=None,skip: int = 0, limit: int = 100) :
    '''_Summary_<br>
        _Lista delle richieste storiche<br>

    __Args:__<br>
        <li>__stato__ (StateProcess): _stato di destinazione del processo di __validazione__ </li>
        <li>__validation_id_ (id, optional): __id__ della richiesta  che effettua il caricamento_. Defaults to Null.</li>
        <li>__skip__ (int, optional): _parametro della paginazione per saltare le righe_. Defaults to 0.</li>
        <li>__limit__ (int, optional): _parametro di paginazione per avere un limite sul numero di record restituiti _. Defaults to 100.</li>

    __Returns:__<br>
        _type_: _json_
        lista delle richieste al director o del worker
    '''

    try:
        async with async_session_Db() as session:
            async with session.begin():
                request_dal = RichiesteDAL(session)
                ret = await request_dal.get_all_requests(id, group_id, skip, limit)
        return ret
    except Exception as e:
        logger.error(f"Error:{e}", stack_info=True)
        return JSONResponse(content={"error": str(e),"group_id":group_id,
                                     "id":id
                                     },
                            status_code=501)


@app.delete("/delete_shape")
async def delete_shape(ID_SHAPE: int):
    """_summary_<br>
                cancellazione funzione<br>
         __Args:__<br>
             <li> function_name (str): _funzione da cancellare_ </li>

        __Returns__:<br>
            _type_: _json_

        """
    async with async_session_Db() as session:
        async with session.begin():
            request_dal = RichiesteDAL(session)
            ret = await request_dal.get_all_requests(ID_SHAPE=ID_SHAPE)
            #cancellazione folder da to_upload
            shutil.rmtree(ret.PATH_SHAPEFILE)
            #cancellazione layer pubblicati
            delete_layers([l.split(".")[0] for l in ret.USERFILE])
            return await request_dal.del_request(ID_SHAPE=ID_SHAPE)

#TODO: servizio per update shape sul db
#TODO: servizio per caricare il python del modello sul db  tabella id-modello-codice-json della sua response


@app.post("/execute_code/")
async def execute_code(group_id:str,model_id: int,shape_id: int,params: dict,mapping_output: dict,code:str=None,language: str=Query(description="Selezionare linguaggio",enum=LIST_LANG) ):
    from config import engine_Db_no_async,CHUNCKSIZE,connection_string
    # Analisi del codice alla ricerca dei parametri %param1%
    params = re.findall(r'%([^%]+)%', code)

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
            mapping_shape = {}
            for tablename,type_dataframe in mapping_shape.items():
                if type_dataframe=="gd.GeoDataFrame":
                    gdf:gd.GeoDataFrame = gd.read_postgis(f"{group_id}.{tablename}",connection_string)
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

            return JSONResponse(status_code=200, content={"layers": layers,"table_name":table_name})
        except Exception as e:
            return JSONResponse(status_code=500, content=f"Errore durante l'esecuzione dello script Python {e}")
    elif language == "r":
        try:
            result,variables=invoke_R(code)
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
            return JSONResponse(status_code=200, content={"layers": layers,"table_name":table_name})
            #return JSONResponse(status_code=200, content={"result": result})
        except Exception as e:
            return JSONResponse(status_code=500, content=f"Errore durante l'esecuzione dello script Python {e}")
    

