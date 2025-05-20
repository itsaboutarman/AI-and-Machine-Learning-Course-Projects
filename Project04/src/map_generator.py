import pandas as pd
from shapely import wkt
from typing import Dict, List

def generate_borders_by_continent(continent: str) -> Dict[str, List[str]]:

    neighbors_df = pd.read_csv('./countries_dataset.csv')
    neighbors_df['geometry'] = neighbors_df['geometry'].apply(wkt.loads)

    continent_df = neighbors_df[neighbors_df['continent'] == continent]

    borders = {}
    for _, row in continent_df.iterrows():
        neighbors = row['neighbors'].split(', ') if isinstance(row['neighbors'], str) else []
        borders[row['iso_a3']] = neighbors

    return borders