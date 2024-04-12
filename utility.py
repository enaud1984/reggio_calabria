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

def get_list_files(shapefile_folder):
    map_files = {}
    list_files = sorted(os.listdir(shapefile_folder), reverse=False)
    for file_name in list_files:
        k = file_name[:-4].lower()
        if k not in map_files or file_name.endswith('.shp'):
            if file_name.endswith('.shp'):
                map_files[k] = file_name
            elif file_name.endswith('.dbf'):
                map_files[k] = file_name
    return map_files
def shapeFile2Postgis(file_zip,conn_str,schema,engine=engine_sinfiDb_no_async):
    try:
        shapefile_folder = unzip(file_zip,"export")
        if not ENABLE_POOL_LOAD:
            return shapeFiles2Postgis(conn_str,schema,engine,shapefile_folder)

        logger.info(f"Caricamento parallelo,file:{file_zip}")
        map_results = {}
        map_files = get_list_files(shapefile_folder)
        list_dbf=[k for k,file_name in map_files.items() if file_name.endswith('.dbf')]
        list_shp=[k for k,file_name in map_files.items() if file_name.endswith('.shp')]
        logger.info(f"Caricamento parallelo:{shapefile_folder}, dbf:{len(list_dbf)},shp:{len(list_shp)}")
        num_thread =int(len(map_files)/2)
        tasks=[]
        start_time_tot = datetime.now()
        pool = ThreadPool(num_thread)
        for k in list_dbf:
            file_name = map_files[k]
            shapefile_path = os.path.join(shapefile_folder, file_name)
            table_name = k  # Usa il nome del file shape come nome della tabella
            task = pool.apply_async(load_dbf_to_postgis, args=(shapefile_path, table_name,conn_str,schema,engine))
            tasks.append(task)
        '''
        pool.close()
        pool.join()
        results = [r.get() for r in tasks if r.get() is not None]
        elapsed = (datetime.now() - start_time_tot).total_seconds()
        logger.info(f"terminati dbf:{len(list_dbf)},dbf time elapsed:{elapsed}")
        num_thread = len(list_shp)
        tasks = []
        pool = ThreadPool(num_thread)
        '''
        for k in list_shp:
            file_name = map_files[k]
            shapefile_path = os.path.join(shapefile_folder, file_name)
            table_name = k  # Usa il nome del file shape come nome della tabella
            task = pool.apply_async(load_shapefile_to_postgis, args=(shapefile_path, table_name,conn_str,schema,engine))
            tasks.append(task)
        pool.close()
        pool.join()
        #res,table_name,elapsed
        results = [r.get() for r in tasks if r.get() is not None]
        for res,table_name,elapsed in results:
            file_name = map_files[table_name]
            if res:
                map_results[file_name]=table_name
            else:
                if "Error" not in map_results:
                    map_results["Error"]=[]
                map_results["Error"].append(file_name)
            if "Stats" not in map_results:
                map_results["Stats"]={}
            map_results["Stats"][table_name]=f"{file_name} elapsed:{elapsed}"
        if "Stats" not in map_results:
            map_results["Stats"]={}
        elapsed=(datetime.now() - start_time_tot).total_seconds()
        map_results["Stats"]["TOTAL"]=f"Total time elapsed:{elapsed}"
        logger.info(f"terminati shp:{len(list_shp)},Total time elapsed:{elapsed}")
        return map_results
    except Exception as e:
        logger.error(f"Error shapeFile2Postgis  error:{e}", exc_info=True)
        print(e)

def shapeFiles2Postgis(conn_str,schema,shapefile_folder,engine=engine_sinfiDb_no_async):
    results={}
    start_time_tot = datetime.now()
    map_files,shapefile_folder,srid_validation,load_type = get_list_files(shapefile_folder)
    for k,file_name in map_files.items():
        shapefile_path = os.path.join(shapefile_folder, file_name)
        table_name = k # Usa il nome del file shape come nome della tabella
        try:
            if file_name.endswith('.shp'):
                res,_,elapsed = load_shapefile_to_postgis(shapefile_path, table_name,conn_str,schema,engine)
            else:
                res,_,elapsed = load_dbf_to_postgis(shapefile_path, table_name,conn_str,schema,engine)
            if res:
                results[file_name]=table_name
            else:
                if "Error" not in results:
                    results["Error"]=[]
                results["Error"].append(table_name)
            if "Stats" not in results:
                results["Stats"]={}
            results["Stats"][table_name]=f"{file_name} elapsed:{elapsed}"
            logger.info(f"caricato {file_name} elapsed:{elapsed}")
        except Exception as e:
            logger.error(f"Error shapeFile2Postgis {shapefile_path} error:{e}", exc_info=True)
            if "Error" in results:
                results["Error"]=[]
            results["Error"].append(F"{e} table_name:{table_name}")
    if "Stats" not in results:
        results["Stats"] = {}
    elapsed=(datetime.now() - start_time_tot).total_seconds()
    results["Stats"]["TOTAL"]=f"Total time elapsed:{elapsed}"
    return results

def load_dbf_to_postgis(shapefile_path,table_name,conn_str,schema,engine):
    # FIX1: I nomi sono presi dai file che non sono gli stessi che crea il validatore infatti usa altri nomi.
    # FIX2: Il campo geometrico è chiamato sempre geometry, quindi quando c'è devo creare un altro campo geometry_2D senza la 'Z'
    try:
        import pandas as pd
        from simpledbf import Dbf5
        start_time = datetime.now()
        dbf = Dbf5(shapefile_path)
        df = dbf.to_dataframe()
        df = df.rename(columns=str.lower)
        map_create, columns, _,columns_list=get_columns_shapefile(shapefile_path,df)
        res = load_df_to_postgres(conn_str,schema,table_name,columns,df,columns_list,engine)
        elapsed=(datetime.now() - start_time).total_seconds()
        logger.info(f"caricato {table_name},elapsed:{elapsed}")
        return res,table_name,elapsed
    except Exception as e:
        logger.error(f"Error load_dbf_to_postgis table {table_name}: {e}")
        elapsed=(datetime.now() - start_time).total_seconds()
        return False,table_name,elapsed


def load_df_to_postgres(conn_str, schema, table_name, columns, df, columns_list, engine):
    # columns=columns.replace("GEOMETRY","geometry")
    create_table_query = f"CREATE TABLE IF NOT EXISTS {schema}.{table_name} ({columns}"
    with psycopg2.connect(conn_str) as conn:
        conn.set_isolation_level(0)
        # Creazione della tabella
        with conn.cursor() as cur:
            # DROP TABELLE CON LO STESSO NOME IN FOREIGN TABLE
            try:
                sql_drop_foreign_table_if_exists = f"DROP FOREIGN TABLE IF EXISTS {schema}.{table_name}"
                cur.execute(sql_drop_foreign_table_if_exists)
                conn.commit()
            except:
                conn.rollback()
                logger.warning(f"No Foreign Table  {schema}.{table_name}")
            try:
                sql_drop_table_if_exists = f"DROP TABLE IF EXISTS {schema}.{table_name}"
                cur.execute(sql_drop_table_if_exists)
                conn.commit()
            except:
                conn.rollback()
                logger.warning(f"No Table  {schema}.{table_name}")
            primary_key = None
            conditions = [
                (("classid", "class_ref"), "(classid,class_ref,group_id)"),
                (("segmentid", "class_ref"), "(segmentid,class_ref,group_id)"),
                (("classid",), "(classid,group_id)"),
                (("segmentid",), "(segmentid,group_id)")
                # ,(("classid", "segmentid"), "(group_id)"),
                # (("class_ref",), "(class_ref,group_id)")
            ]
            primary_key = None
            for cols, format_str in conditions:
                if all(col in columns_list for col in cols):
                    primary_key = format_str
            if primary_key:
                create_table_query += f" ,CONSTRAINT {table_name}_pk PRIMARY KEY {primary_key})"
            else:
                create_table_query += ")"
            cur.execute(create_table_query)
            conn.commit()
            # Caricamento dei dati nella tabella
            if hasattr(df, "to_postgis"):
                df.to_postgis(table_name, engine, if_exists='replace', index=False, schema=schema,
                              chunksize=CHUNCKSIZE)
            else:
                df.to_sql(table_name, engine, if_exists='replace', index=False, schema=schema, chunksize=CHUNCKSIZE)
            engine.dispose()
            return True


def get_columns_shapefile(shapefile_path, gdf):
    columns_list = list(gdf.columns)
    if hasattr(gdf, "crs"):
        crs_string = str(gdf.crs)
        geometry_type = gdf.geometry.geom_type.unique()[0]
        # verifica se ci sta la coordinata Z:
        has_z_coordinate = gdf.geometry.has_z.all()
        if has_z_coordinate:
            geometry_type += "Z"
        logger.info(f"carico {shapefile_path} geometry_type:{geometry_type}")
        srid=None
        if "AUTHORITY" in crs_string:
            srid = int(crs_string.split("EPSG")[-1].replace("\"", "").replace("]", "").replace(",", ""))
        representation = f"geometry({geometry_type}"
    else:
        representation = "geometry"
    postgis_types_mapping = {
        'object': 'text',
        'int64': 'integer',
        'float64': 'double precision',
        'float32': 'double precision',
        'int32': 'integer',
        'int16': 'integer',
    }
    gdf_types_list = []
    for dtype in gdf.dtypes:
        if dtype == "geometry":
            tipo = representation
        else:
            tipo = postgis_types_mapping[str(dtype)]
        gdf_types_list.append(tipo)
    gdf_types_list.append("text")  # group_id
    # se esiste un campo di tipo geometry, aggiungere un campo "geometry" tipo geometry("tipo senza Z",25832)
    for ele in gdf_types_list:
        if ele.startswith("geometry") and "Z," in ele.upper():
            comma_index = ele.find(",")
            if comma_index != -1:
                number_str = ele[comma_index + 1:-1]
                ele_new = ele.replace("Z", "").replace("z", "").replace(number_str, "25832")
                columns_list.append("geometry_2D")
                gdf_types_list.append(ele_new)
    map_create = {key: value for key, value in zip(columns_list, gdf_types_list)}
    map_create_date = {}
    for c, t in map_create.items():
        if c.startswith("data_"):
            map_create_date[c] = "date"
    map_create.update(map_create_date)
    columns = ", ".join([f"{column} {dtype}" for column, dtype in map_create.items()])
    return map_create, columns, srid, columns_list

def load_shapefile_to_postgis(shapefile_path,table_name,conn_str,schema,engine,):
    try:
        import geopandas as gpd
        start_time = datetime.now()
        gdf = gpd.read_file(shapefile_path)
        gdf = gdf.rename(columns=str.lower)
        #gdf.set_crs(f"EPSG:{srid}", allow_override=True,inplace=True)
        geometry_type = gdf.geometry.geom_type.unique()[0]
        if geometry_type is None:
            logger.error(f"{shapefile_path} non la geometria valorizzata"  )
            return False
        map_create, columns, srid,columns_list=get_columns_shapefile(shapefile_path,gdf)
        elapsed=(datetime.now() - start_time).total_seconds()
        res = load_df_to_postgres(conn_str,schema,table_name,columns,gdf,columns_list,engine)
        return res,table_name,elapsed
    except Exception as e:
        elapsed=(datetime.now() - start_time).total_seconds()
        logger.error(f"Error creating table {table_name}: {e},map_create:{map_create}")
        return False,table_name,elapsed