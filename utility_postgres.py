import logging
import datetime
import struct
from multiprocessing.pool import ThreadPool

import psycopg2

from config import engine_sinfiDb_no_async, APP, CHUNCKSIZE
import os

from utility import find_specTable, change_column_types

logger = logging.getLogger(APP)
from simpledbf import Dbf5


def get_now():
    return datetime.datetime.now()

class Dbf_wrapper(Dbf5):

    def _get_recs(self, chunk=None):
        '''Generator that returns individual records.

        Parameters
        ----------
        chunk : int, optional
            Number of records to return as a single chunk. Default 'None',
            which uses all records.
        '''
        if chunk == None:
            chunk = self.numrec

        for i in range(chunk):
            # Extract a single record
            record = struct.unpack(self.fmt, self.f.read(self.fmtsiz))
            # If delete byte is not a space, record was deleted so skip
            if record[0] != b' ':
                continue

                # Save the column types for later
            self._dtypes = {}
            result = []
            for idx, value in enumerate(record):
                name, typ, size = self.fields[idx]
                if name == 'DeletionFlag':
                    continue

                # String (character) types, remove excess white space
                if typ == "C":
                    if name not in self._dtypes:
                        self._dtypes[name] = "str"
                    value = value.strip()
                    # Convert empty strings to NaN
                    if value == b'':
                        value = self._na
                    else:
                        value = value.decode(self._enc)
                        # Escape quoted characters
                        if self._esc:
                            value = value.replace('"', self._esc + '"')

                # Numeric type. Stored as string
                elif typ == "N":
                    # A decimal should indicate a float
                    if b'.' in value:
                        if name not in self._dtypes:
                            self._dtypes[name] = "float"
                        value = float(value)
                    # No decimal, probably an integer, but if that fails,
                    # probably NaN
                    else:
                        try:
                            value = int(value)
                            if name not in self._dtypes:
                                self._dtypes[name] = "int"
                        except:
                            # I changed this for SQL->Pandas conversion
                            # Otherwise floats were not showing up correctly
                            value = float('nan')

                # Date stores as string "YYYYMMDD", convert to datetime
                elif typ == 'D':
                    try:
                        y, m, d = int(value[:4]), int(value[4:6]), \
                            int(value[6:8])
                        if name not in self._dtypes:
                            self._dtypes[name] = "date"
                    except:
                        value = self._na
                    else:
                        if y==0 or m==0 or d==0:
                            value = None
                        else:
                            value = datetime.date(y, m, d)

                # Booleans can have multiple entry values
                elif typ == 'L':
                    if name not in self._dtypes:
                        self._dtypes[name] = "bool"
                    if value in b'TyTt':
                        value = True
                    elif value in b'NnFf':
                        value = False
                    # '?' indicates an empty value, convert this to NaN
                    else:
                        value = self._na

                # Floating points are also stored as strings.
                elif typ == 'F':
                    if name not in self._dtypes:
                        self._dtypes[name] = "float"
                    try:
                        value = float(value)
                    except:
                        value = float('nan')

                else:
                    err = 'Column type "{}" not yet supported.'
                    raise ValueError(err.format(value))

                result.append(value)
            yield result


def shapeFile2Postgis(validation_id,map_files,map_tables_edited,shapefile_folder,group_id,conn_str,schema=None,
                      engine=engine_sinfiDb_no_async, srid=None,load_type="append"):
    from importerLayers import publish_layers
    try:
        if not schema:
            schema=group_id
        logger.info(f"Caricamento parallelo, srid={srid}, load_type={load_type}")

        map_results = {}
        list_dbf=[k for k, file_name in map_files.items() if file_name.endswith('.dbf')]
        list_shp=[k for k, file_name in map_files.items() if file_name.endswith('.shp')]
        logger.info(f"Caricamento parallelo:{shapefile_folder}, dbf:{len(list_dbf)},shp:{len(list_shp)}")
        num_thread =int(len(map_files)/2)+1
        tasks=[]
        start_time_tot = get_now()
        pool = ThreadPool(num_thread)
        for k in list_dbf:
            file_name = map_files[k]
            shapefile_path = os.path.join(shapefile_folder, file_name)
            table_name = k  # Usa il nome del file shape come nome della tabella
            task = pool.apply_async(load_dbf_to_postgis, args=(shapefile_path,map_tables_edited, table_name,conn_str,schema,engine,group_id,load_type,srid))
            tasks.append(task)

        for k in list_shp:
            file_name = map_files[k]
            shapefile_path = os.path.join(shapefile_folder, file_name)
            table_name = k  # Usa il nome del file shape come nome della tabella
            task = pool.apply_async(load_shapefile_to_postgis, args=(shapefile_path, map_tables_edited, table_name,conn_str,schema,engine,group_id,load_type,srid))
            tasks.append(task)
        pool.close()
        pool.join()

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
        elapsed=(get_now() - start_time_tot).total_seconds()
        map_results["Stats"]["TOTAL"]=f"Total time elapsed:{elapsed}"
        logger.info(f"terminati shp:{len(list_shp)},Total time elapsed:{elapsed}")
        layers=[table for table in list_shp]
        publish_layers(group_id,layers=layers,with_view=True)
        return map_results
    except Exception as e:
        logger.error(f"Error shapeFile2Postgis  validation_id:{validation_id} error:{e}", exc_info=True)
        print(e)


def load_dbf(shapefile_path, table_name,group_id=None,srid_validation=None):
    dbf = Dbf_wrapper(shapefile_path)
    df = dbf.to_dataframe()
    df = df.rename(columns=str.lower)
    if group_id:
        df['group_id']=group_id
    map_create, columns, _, columns_list = get_columns_shapefile(shapefile_path,table_name,df,srid_validation)
    return map_create, columns, _, columns_list,df

def load_dbf_to_postgis(shapefile_path,map_tables_edited,table_name,conn_str,schema,engine,group_id,load_type,srid_validation):
    try:
        #import pandas as pd
        start_time = get_now()
        map_create, columns, _, columns_list,df=load_dbf(shapefile_path,table_name,group_id,srid_validation)
        json_types=find_specTable(map_tables_edited,table_name)
        df=change_column_types(df, json_types)
        res = load_df_to_postgres(load_type,conn_str,schema,table_name,columns,df,columns_list,engine)
        elapsed=(get_now() - start_time).total_seconds()
        logger.info(f"caricato {table_name},map_create:{map_create},elapsed:{elapsed}")
        return res,table_name,elapsed
    except Exception as e:
        logger.error(f"Error load_dbf_to_postgis table {table_name}: {e}",stack_info=True)
        elapsed=(get_now() - start_time).total_seconds()
        return False,table_name,elapsed

def load_df_to_postgres(load_type,conn_str,schema,table_name,columns,df,columns_list,engine):

    if load_type=="strict":  #caso in cui si ricrea la tabella
        #columns=columns.replace("GEOMETRY","geometry")
        create_table_query = f"CREATE TABLE IF NOT EXISTS {schema}.{table_name} ({columns}"
        with psycopg2.connect(conn_str) as conn:
            conn.set_isolation_level(0)
            # Creazione della tabella
            with conn.cursor() as cur:
                #DROP TABELLE CON LO STESSO NOME IN FOREIGN TABLE
                try:
                    sql_drop_foreign_table_if_exists=f"DROP FOREIGN TABLE IF EXISTS {schema}.{table_name} CASCADE"
                    cur.execute(sql_drop_foreign_table_if_exists)
                    conn.commit()
                except:
                    conn.rollback()
                    logger.warning(f"No Foreign Table  {schema}.{table_name}")
                try:
                    sql_drop_table_if_exists = f"DROP TABLE IF EXISTS {schema}.{table_name} CASCADE"
                    cur.execute(sql_drop_table_if_exists)
                    conn.commit()
                except:
                    conn.rollback()
                    logger.warning(f"No Table  {schema}.{table_name}",stack_info=True)

                #if len(keys)>0:
                #     keys.append("group_id")
                #     primary_key="("+",".join(keys)+")"
                #     create_table_query+=f" ,CONSTRAINT {table_name}_pk PRIMARY KEY {primary_key})"
                # else:
                #     create_table_query+=")"

                create_table_query+=")"
                cur.execute(create_table_query)
                conn.commit()
                # Caricamento dei dati nella tabella
                if hasattr(df,"to_postgis"):
                    df.to_postgis(table_name, engine, if_exists='replace', index=False, schema=schema,chunksize=CHUNCKSIZE)
                else:
                    df.to_sql(table_name, engine, if_exists='replace', index=False, schema=schema,chunksize=CHUNCKSIZE)

                engine.dispose()
                return True
    else:
        table_name_temp =f"temp_{table_name}"
        create_table_query = f"CREATE TABLE IF NOT EXISTS {schema}.{table_name_temp} ({columns}"
        if hasattr(df,"to_postgis"):
            df.to_postgis(table_name_temp, engine, if_exists='replace', index=False, schema=schema,chunksize=CHUNCKSIZE)
        else:
            df.to_sql(table_name_temp, engine, if_exists='replace', index=False, schema=schema,chunksize=CHUNCKSIZE)
        engine.dispose()
        join_columns=','.join(columns_list)
        join_temp_columns=','.join([f"{table_name_temp}.{k}" for k in columns_list])
        join_excluded=','.join([f"{k} = EXCLUDED.{k}" for k in columns_list if k not in ["class_id","class_ref","segmentid","groupid"]])

        upsert_query = f"""
            INSERT INTO {table_name} ({join_columns})
            SELECT {join_temp_columns}
            FROM {table_name_temp}
            ON CONFLICT ({table_name}_pk) DO UPDATE
            SET {join_excluded}
        """
        with engine.connect() as conn:
            conn.execute(upsert_query)

        with psycopg2.connect(conn_str) as conn:
            conn.set_isolation_level(0)
            # Creazione della tabella
            with conn.cursor() as cur:
                try:
                    sql_drop_table_if_exists = f"DROP TABLE IF EXISTS {schema}.{table_name_temp}"
                    cur.execute(sql_drop_table_if_exists)
                    conn.commit()
                except:
                    conn.rollback()
                    logger.warning(f"No Table  {schema}.temp_{table_name}",stack_info=True)
        return True

def get_columns_shapefile(shapefile_path,table_name,gdf, srid = None):
    columns_list = list(gdf.columns)
    columns_list.append("group_id")
    if hasattr(gdf,"crs"):
        crs_string = str(gdf.crs)
        geometry_type = gdf.geometry.geom_type.unique()[0]
        # verifica se ci sta la coordinata Z:
        has_z_coordinate = gdf.geometry.has_z.all()
        if has_z_coordinate:
            geometry_type += "Z"
        logger.info(f"carico {shapefile_path} geometry_type:{geometry_type}")

        if "AUTHORITY" in crs_string  and srid is None:
            srid = int(crs_string.split("EPSG")[-1].replace("\"", "").replace("]", "").replace(",", ""))
        representation = f"geometry({geometry_type},{srid})"
    else:
        representation = f"geometry"
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

    map_create.update(map_create_date)
    columns = ", ".join([f"{column} {dtype}" for column, dtype in map_create.items()])
    return map_create,columns,srid,columns_list

def load_shapefile_to_postgis(shapefile_path,map_tables_edited,table_name,conn_str,schema,engine,group_id,load_type,srid_validation):
    map_create={}
    try:
        resp, columns, gdf, columns_list, start_time, elapsed,map_create = load_shapefile(shapefile_path, table_name, group_id, srid_validation)
        json_types=find_specTable(map_tables_edited,table_name)
        gdf=change_column_types(gdf, json_types)
        if not resp:
            return False,table_name,elapsed
        res = load_df_to_postgres(load_type,conn_str,schema,table_name,columns,gdf,columns_list,engine)
        return res,table_name,elapsed
    except Exception as e:
        elapsed=(get_now() - start_time).total_seconds()
        logger.error(f"Error creating table {table_name}: {e},map_create:{map_create}")
        return False,table_name,elapsed

def load_shapefile(shapefile_path,table_name,group_id=None,srid_validation=None):
    import geopandas as gpd
    start_time = get_now()
    srid = srid_validation
    gdf = gpd.read_file(shapefile_path)
    gdf = gdf.rename(columns=str.lower)
    if srid is not None:
        gdf.set_crs(f"EPSG:{srid}", allow_override=True,inplace=True)
    if group_id:
        gdf['group_id']=group_id
    geometry_type = gdf.geometry.geom_type.unique()[0]
    if geometry_type is None:
        elapsed=(get_now() - start_time).total_seconds()
        logger.error(f"{shapefile_path} non la geometria valorizzata"  )
        return False, table_name, elapsed
    map_create, columns, srid, columns_list = get_columns_shapefile(shapefile_path,table_name,gdf,srid_validation)
    elapsed = (get_now() - start_time).total_seconds()
    return True, columns, gdf, columns_list, start_time, elapsed,map_create
