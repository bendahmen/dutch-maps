#!/usr/bin/env python
"""
Read data on Dutch gemeentes and Natura2000 areas and calculate minimum
distance between each gemeente and Natura2000 area. Then save output
to a CSV file.
"""

import geopandas as gpd

def main():
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
    print('Data saved to ../data/output/gemeente_natura2000_distance.csv')

if __name__ == '__main__':
    main()