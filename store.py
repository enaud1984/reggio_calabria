import os
import pickle
import geopandas as gpd

class Data:
    input = {}
    def __init__(self,tables) -> None:
        input={}
        for table in tables:
            pickle_file =os.path.join("data",f"{table}.pickle")
            if os.path.exists(pickle_file):
                with open(pickle_file, 'rb') as f:
                    gdf=pickle.load(f)
            else:
                filename = os.path.join("data",f"{table}.shp")
                gdf = gpd.read_file(filename)
                gdf = gdf.rename(columns=str.lower)
                with open(pickle_file, 'wb') as f:
                    pickle.dump(gdf,f)
            input[table]= gdf
        self.input=input
        
    def get_table(self,name):
        return self.input[name]