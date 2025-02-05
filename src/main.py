#!/usr/bin/env python
"""
Read data on Dutch gemeentes and Natura2000 areas and calculate minimum
distance between each gemeente and Natura2000 area, and nitrogen
deposition levels. Then save output to a CSV file.
"""

import geopandas as gpd

def main():
    # --- Read data ---

    # read Dutch gemeentes
    gemeente_borders = gpd.read_file('../data/gemeente_borders.json')
    # convert to common CRS
    gemeente_borders = gemeente_borders.to_crs(epsg=28992)

    # read Natura2000 areas
    natura2000 = gpd.read_file('../data/geopackage-monitor_2025-01-06/natura2000-area-receptor-nitrogen-loads.gpkg', layer='m23')
    # convert to common CRS
    natura2000 = natura2000.to_crs(epsg=28992)

    # --- Filter Data ---

    # filter out gemeentes in the Netherlands
    gemeente_borders = gemeente_borders[gemeente_borders['rubriek']=='gemeente']

    # filter out depositions data from 2020
    natura2000 = natura2000[natura2000['year']==2020]

    # --- Manipulate Data ---

    # calculate gemeente centroids
    gemeente_borders['centroid_geometry'] = gemeente_borders.geometry.centroid
    gemeente_centroids = gpd.GeoDataFrame(
        gemeente_borders.drop(columns='geometry'), 
        geometry='centroid_geometry', 
        crs=gemeente_borders.crs
    )

    # calculate maximum deposition for each Natura2000 area
    natura2000['max_deposition'] = natura2000.groupby('natura2000_area_code')['deposition'].transform('max')

    # Use sjoin_nearest to find for each centroid the nearest hexagon from depositions.
    # We include the distance, deposition and max_deposition columns.
    nearest = gpd.sjoin_nearest(gemeente_centroids, natura2000[['geometry', 'deposition', 'max_deposition']],how="left",distance_col="distance")

    # --- Save Data ---

    # save to CSV
    nearest[['statcode', 'statnaam', 'distance', 'deposition', 'max_deposition']].to_csv('../data/output/gemeente_natura2000_distance_and_depositions.csv', index=False)
    print('Data saved to ../data/output/gemeente_natura2000_distance_and_depositions.csv')

def distances():
    """
    Distance between municipalities and Natura2000 areas using
    official municipality data. The more updated version of this
    has data on emissions as well.
    """

    # --- Read data ---

    # read Dutch gemeentes
    gemeente_borders = gpd.read_file('../data/gemeente_borders.json')
    # convert to common CRS
    gemeente_borders = gemeente_borders.to_crs(epsg=28992)

    # read Natura2000 areas
    natura2000 = gpd.read_file('../data/Natura2000_end2019_shp/Natura2000_end2019_epsg3035.shp')
    # convert to common CRS
    natura2000 = natura2000.to_crs(epsg=28992)

    # --- Filter Data ---

    # filter out gemeentes in the Netherlands
    gemeente_borders = gemeente_borders[gemeente_borders['rubriek']=='gemeente']

    # filter out Natura2000 areas in the Netherlands
    natura2000 = natura2000[natura2000['MS']=='NL']

    # --- Manipulate Data ---

    # calculate gemeente centroids
    gemeente_borders['centroid'] = gemeente_borders.centroid

    # calculate minimum distance between gemeente and Natura2000 area
    def min_distance(point, areas):
        return areas.distance(point).min()
    gemeente_borders['distance'] = gemeente_borders['centroid'].apply(min_distance, areas=natura2000.geometry)

    # --- Save Data ---

    # save to CSV
    gemeente_borders[['statcode', 'statnaam', 'distance']].to_csv('../data/output/gemeente_natura2000_distance.csv', index=False)

if __name__ == '__main__':
    main()