# Import the library
import datetime
import logging
from collections import namedtuple
from datetime import datetime

from geo.Geoserver import Geoserver

from config import APP, GEOSERVER_ADMIN_PASSWORD, GEOSERVER_ADMIN_USER, GEOSERVER_DB_PORT, GEOSERVER_DB_SERVICES, \
    GEOSERVER_LOCATION, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB

logger = logging.getLogger(APP)

class GeoserverManager:
    list_group_layers=[]
    list_view =[]
    
    def __init__(self,url_geo=GEOSERVER_LOCATION,username=GEOSERVER_ADMIN_USER, password=GEOSERVER_ADMIN_PASSWORD):
        # Initialize the library
        url_geo=url_geo[:-1] if url_geo.endswith("/") else url_geo
        logger.info(f"GeoserverManager  url_geo: {url_geo} username:{username}")
        self.geo = Geoserver(url_geo, username=username, password=password)
        #cat = Catalog(f'{url_geo}/rest/',username='admin', password='geoserver')
        self.workspace=None
    
    def create_ws(self,group_id,db: str = "postgres",
                    host: str = GEOSERVER_DB_SERVICES,
                    port: int = GEOSERVER_DB_PORT,
                    schema: str = "public",
                    pg_user: str = POSTGRES_USER,
                    pg_password: str = POSTGRES_PASSWORD,
                    ): 
        # For creating workspace
        self.workspace = f"{group_id}"
        try:
            self.geo.get_workspace(workspace= self.workspace) 
        except:
            self.res_schema = self.geo.create_workspace(workspace= self.workspace)
        self.db: str = db
        self.host: str = host
        self.port: int = int(port)
        self.schema: str = schema,
        self.pg_user: str = pg_user
        self.pg_password: str = pg_password
                    
    
    def create_layers(self,group_id,db,layers:list, schema=None,
                    overwrite: bool = False,
                    expose_primary_keys: str = "true",
                    description: str = None):
        self.group_id = group_id 
        self.storename=f"{group_id}_ds"
        if description is None:
            description=f"create_layers group_id: {group_id} at {datetime.now()} layers:{layers}"
        if schema is not None:
            self.schema=schema
        else:
            self.schema=group_id
        logger.info(f"create_layers  group_id: {group_id} layers:{layers}")
        check = self.geo.get_datastores(workspace= self.workspace) 
        # For uploading raster data to the geoserver
        #check = self.geo.get_featurestors(store_name=self.storename,workspace= self.workspace) 
        self.data_stores = namedtuple("Datastores",list(check.keys()))(**check)
        if  len(self.data_stores.dataStores)==0:
            self.res_store=self.geo.create_featurestore(store_name=self.storename,
            workspace=self.workspace,
            db=db,
            host= self.host,
            port= self.port,
            schema= self.schema,
            pg_user= self.pg_user,
            pg_password=self.pg_password,
            overwrite=overwrite,
            expose_primary_keys=expose_primary_keys,
            description=description
            )					
        """
            evictor_run_periodicity: int | None = 300,
            max_open_prepared_statements: int | None = 50,
            encode_functions: str | None = "false",
            primary_key_metadata_table: str | None = None,
            batch_insert_size: int | None = 1,
            preparedstatements: str | None = "false",
            loose_bbox: str | None = "true",
            estimated_extends: str | None = "true",
            fetch_size: int | None = 1000,
            validate_connections: str | None = "true",
            support_on_the_fly_geometry_simplification: str | None = "true",
            create_database: str | None = "false",
            connection_timeout: int | None = 20,
            min_connections: int | None = 1,
            max_connections: int | None = 10,
            evictor_tests_per_run: int | None = 3,
            test_while_idle: str | None = "true",
            max_connection_idle_time: int | None = 300
        """
        map_layers =self.getfeaturestores(workspace=self.workspace)
        if map_layers is not None:
            l = None
            try:
                self.res_layers={}
                for l in layers:
                    if l not in map_layers:
                        self.res_layers[l]=self.geo.publish_featurestore(workspace=self.workspace, 
                            store_name=self.storename, 
                            pg_table=l,
                            title=f"{group_id}.{l}"
                        ) 
            except Exception as e:
                logger.error(f"Error publish_featurestore {l} group_id:{group_id} error:{e}", exc_info=True)
                print(e)
     
            self.map_layers = self.res_layers
        else:
            self.map_layers = map_layers
        map_layer_group = {}
        self.list_view = [t for t in self.map_layers if t.startswith("v_")]
        list_group_layers = [t.split("_")[1] for t in self.map_layers if not t.startswith("v_") and len(t.split("_"))>1]
        if len(self.list_group_layers)==0:
            list_group_layers = list(set(list_group_layers))
            self.list_group_layers = list_group_layers
        else:
            list_group_layers = self.list_group_layers   
        
        for name in layers:
            for name_group in list_group_layers:
                if f"_{name_group}" in name:
                    if name_group not in map_layer_group:
                        map_layer_group[name_group] = []
                    map_layer_group[name_group].append(name)
        
        for name in map_layer_group:
            ll = map_layer_group[name]
            layergroup_name=f"{self.workspace}_{name}"
            if "meta" in layers:
                ll = ["meta"]+ll
            if "v_meta" in layers:
                ll = ["v_meta"]+ll
                layergroup_name=f"{self.workspace}_{name}_view"
            layer_groups = self.geo.get_layergroups(workspace=self.workspace)
            
            if "layerGroups" in layer_groups and type(layer_groups["layerGroups"])==dict and type(layer_groups["layerGroups"].get("layerGroup"))==list and len(layer_groups["layerGroups"].get("layerGroup"))>0:
                layer_groups = {l["name"]:l for l in layer_groups["layerGroups"]["layerGroup"] }
            else:
                layer_groups = {}
            try:
                if layer_groups.get(f"{group_id}.{name}") is None:
                    self.geo.create_layergroup( name= layergroup_name,
                                    mode= "single",
                                    title= "geoserver-rest layer group",
                                    abstract_text = "A new layergroup created with ge",
                                    layers=[f"{group_id}.{l}" for l in ll],
                                    workspace=self.workspace)
                else:
                    layer_group = layer_groups.get(f"{group_id}.{name}")
                    logger.info(f"exists  group_id: {group_id} layer_group:{layer_group}")
            except Exception as e:
                logger.error(f"Error create_layers  group_id:{group_id} error:{e}", exc_info=True)
                print(e)
        #todo: verificare che ci sono delle tabelle aggiuntive nella validazione 
        #self.geo.add_layer_to_layergroup(layer_name=name,layer_workspace=self.workspace, layergroup_name=layergroup_name,layergroup_workspace= self.workspace)
            
    def getfeaturestores(self,workspace):
        res = {}
        layers =self.geo.get_layers(workspace=workspace)['layers']
        if len(layers):
            for l in layers['layer']:
                res[l["name"]]=l
        return res
        
    def delete_ws(self,group_id,workspace,layers:list=[]):
        self.workspace = f"{group_id}"
        self.storename=f"{group_id}_ds"
        # delete layer
        self.res_del_layers={layer_name:self.geo.delete_layer(
                layer_name=layer_name, workspace=self.workspace
            ) 
            for layer_name in layers
        }
        # delete style file
        #geo.delete_style(style_name='kamal2', workspace='demo')
        self.res_delete_store=self.geo.delete_featurestore(featurestore_name=self.storename, workspace=workspace)
        self.res_delete_ws=self.geo.delete_workspace(workspace=workspace)

    def reload(self):
        # Reloads the GeoServer catalog and configuration from disk. This operation is used in cases where an external tool has modified the on-disk configuration. This operation will also force GeoServer to drop any internal caches and reconnect to all data stores.
        return self.geo.reload()

    def reload(self):
        # Resets all store, raster, and schema caches. This operation is used to force GeoServer to drop all caches and store connections and reconnect to each of them the next time they are needed by a request. This is useful in case the stores themselves cache some information about the data structures they manage that may have changed in the meantime.
        return self.geo.reset()

def publish_layers(group_id,layers:list,dest_db:str=POSTGRES_DB,with_view=True):
    gs=GeoserverManager()
    gs.create_ws(group_id=group_id)
    gs.create_layers(group_id,dest_db,layers=layers)
    stores = gs.getfeaturestores(group_id)
    return stores

def delete_layers(group_id,layers:list):
    gs=GeoserverManager()
    logger.info(f"delete_layers  group_id: {group_id} layers:{layers}")
    gs.delete_ws(group_id,group_id,layers=layers)
    return gs.getfeaturestores(group_id)

if __name__=="__main__":
    #group_id="acantho"
    #layers:list=["meta",#"infr_rt_estensione_p",
    #    "nd_com","tr_com","tr_com_tr_com_tra_sg"]
    group_id="tim"
    layers:list=['infr_rt_estensione_l', 'infr_rt_estensione_p', 'meta']
    res=publish_layers(group_id,layers=layers,dest_db=POSTGRES_DB)
    print(f"res {res}")