import logging
import os
import re
import shutil
import subprocess
import traceback
from datetime import datetime

from starlette.responses import JSONResponse

from DAO import CodeInput, ColumnResponse, MapTables
from config import APP, POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, PATH_TO_UPLOAD, \
    LIST_SRID, async_session_Db

from fastapi import FastAPI, UploadFile, File, Query

from importerLayers import delete_layers
from richieste_dal import RichiesteDAL
from utility import unzip, get_map_files, get_md5
from utility_R import invoke_R
from utility_postgres import shapeFile2Postgis, load_dbf, load_shapefile

app = FastAPI(summary= "Applicativo per la gestione di file shape",
              description="""
        """,
              version= "0.0.1")

logger = logging.getLogger(APP)

@app.put("/upload_zip")
async def upload_zip_file(file: UploadFile = File(...)):
    try:
        file_path_zip=os.path.join(PATH_TO_UPLOAD,str(file.filename))
        # Sposta il file nella cartella di destinazione
        with open(file_path_zip, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        #unzip file
        shapefile_folder=unzip(file_path_zip,PATH_TO_UPLOAD)
        os.remove(file_path_zip)
        mapping_fields = MapTables(data=[])
        list_files=[]
        for root, dirs, files in os.walk(shapefile_folder):
            for file in files:
                file_path=os.path.join(root, file)
                table_name=None
                map_create=None
                if file.endswith('.dbf'):
                    list_files.append(file)
                    table_name=file.split(".")[0]
                    map_create, columns, _, columns_list,df = load_dbf(file_path, table_name,group_id=None,srid_validation=None)
                if file.endswith('.shp'):
                    list_files.append(file)
                    table_name=file.split(".")[0]
                    res, columns, gdf, columns_list, start_time, elapsed,map_create=load_shapefile(file_path,table_name,group_id=None,srid_validation=None)
                if map_create and table_name:
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

        async with async_session_Db() as sessionpg:
            async with sessionpg.begin():
                request_dal = RichiesteDAL(sessionpg)
                md5_zip=get_md5(file.filename)
                res_PostGres = await request_dal.create_request(ID=None,
                                                                SHAPEFILE=file.filename,
                                                                DATE_UPLOAD=datetime.now(),
                                                                DATA_LOAD=None,
                                                                DATA_EXECUTION=None,
                                                                STATUS="UPLOAD ZIP",
                                                                GROUP_ID=None,
                                                                PATH_SHAPEFILE=shapefile_folder,
                                                                MD5=md5_zip,
                                                                USERFILE=",".join(list_files),
                                                                LOAD_TYPE=None,
                                                                ESITO="OK",
                                                                RESULTS={})

                print(f"OK WRITE ON SINFIDB, VALIDATION_ID: {res_PostGres.ID}")

        return JSONResponse(content=str(mapping_fields.model_dump_json()), status_code=200)
    except Exception as e:
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
        return JSONResponse(content={"result": result,"esito":"OK"}, status_code=201)
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
async def delete_shape(id: int):
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
            ret = await request_dal.get_all_requests(id=id)
            shutil.rmtree(ret.PATH_SHAPEFILE)
            delete_layers()
            return await request_dal.del_request(id=id)

#TODO: servizio per cancellazione shape sul db
#TODO: servizio per update shape sul db
#TODO: servizio per caricare il python del modello sul db  tabella id-modello-codice-json della sua response


@app.post("/execute_code/")
async def execute_code(code_input: CodeInput):
    # Controllo se il linguaggio è supportato
    if code_input.language not in ["python", "r"]:
        return JSONResponse(status_code=400, content="Linguaggio non supportato")

    # Analisi del codice alla ricerca dei parametri %param1%
    params = re.findall(r'%([^%]+)%', code_input.code)

    # Sostituzione dei parametri con i valori forniti dall'utente
    for param in params:
        value=code_input.params[param]
    code_input.code = code_input.code.replace(f'%{param}%', value)

    # Esecuzione del codice
    if code_input.language == "python":
        try:
            variables = {}
            exec(code_input.code, {}, variables)
            df_out=""
            #df_out=cercare su code_input.data il nome della variabile con df_out = True
            df_result = variables[df_out]


            #return JSONResponse(status_code=200, content={"result": str(result.show(20))})
        except Exception as e:
            return JSONResponse(status_code=500, content=f"Errore durante l'esecuzione dello script Python {e}")
    elif code_input.language == "r":
        try:
            result=invoke_R(code_input.code)
            #return JSONResponse(status_code=200, content={"result": result})
        except Exception as e:
            return JSONResponse(status_code=500, content=f"Errore durante l'esecuzione dello script Python {e}")
    #TODO:pubblicazione su geoserver

