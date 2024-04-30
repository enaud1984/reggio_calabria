import pandas as pd
import geopandas as gpd
import numpy as np
pippo=eval(os.getenv("PIPPO"),"condotte"))

#condotte = gpd.read_file(shapefile_path)
#condotte = condotte.rename(columns=str.lower)
df = pd.DataFrame({'a': ['abc', 'def', 'ghi', 'kjl'],
                   'b': [2, 5, 7, 8],
                   'c': [1.2, 3, 4, 6]})
num_cols = [col for col in df.columns if df[col].dtype in [np.int64, np.float64]]
quadratic_cols = [tuple(sorted((i,j))) for i in num_cols for j in num_cols]
quad_col_pairs = list(set(quadratic_cols))

for col_pair in quad_col_pairs:
    col1, col2 = col_pair
    quadratic_col = '{}*{}'.format(*col_pair)
    df[quadratic_col] = df[col1] * df[col2]
pippo["flusso"]=df[quadratic_col] 
print(pippo.columns)
df_out=df[quadratic_col] 