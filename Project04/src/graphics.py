import geopandas as gpd
import pandas as pd
from shapely import wkt
from typing import Dict
import matplotlib.pyplot as plt

def draw_colored_map(solution: Dict[str, str], gdf: gpd.GeoDataFrame, continent: str, assignments_number: int) -> None:

    # Filter for the selected continent and assign colors
    selected_continent = gdf[gdf['continent'] == continent].copy()
    selected_continent['color'] = selected_continent['iso_a3'].apply(lambda x: solution.get(x, 'lightgrey'))
    
    fig, ax = plt.subplots(1, figsize=(12, 12))
    selected_continent.plot(ax=ax, color=selected_continent['color'], edgecolor='black')
    
    # Set map boundaries
    minx, miny, maxx, maxy = selected_continent.total_bounds
    if continent == "Europe":
        ax.set_xlim(-40, 60)
        ax.set_ylim(35, 80)
        text_x, text_y = -40, 82
    else:
        ax.set_xlim(minx - 1, maxx + 1)
        ax.set_ylim(miny - 1, maxy + 1)
        text_x, text_y = minx, maxy + 2

    # Annotate countries and display the assignment number
    for idx, row in selected_continent.iterrows():
        if row['iso_a3'] in solution:
            plt.text(row.geometry.centroid.x, row.geometry.centroid.y, row['iso_a3'], fontsize=6, ha='center', va='center')
    plt.text(text_x, text_y, f"Assignment Number: {assignments_number}", fontsize=12, ha='left', va='center')
    plt.show()

def draw(continent: str, solution: Dict[str, str], assignments_number: int) -> None:
    neighbors_df = pd.read_csv('./countries_dataset.csv')
    neighbors_df['geometry'] = neighbors_df['geometry'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(neighbors_df, geometry='geometry')
    
    draw_colored_map(solution, gdf, continent, assignments_number)