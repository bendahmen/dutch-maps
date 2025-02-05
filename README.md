# dutch-maps
Build a dataset that contains the distance to the next Natura2000 area for each Dutch Gemeente.

main.py: Read data on Dutch gemeentes and Natura2000 areas and calculate minimum
distance between each gemeente and Natura2000 area. Then save output
to a CSV file.

Data sources:
    - gemeente_borders.json: 
        - Link: https://www.nationaalgeoregister.nl/geonetwork/srv/dut/catalog.search#/metadata/effe1ab0-073d-437c-af13-df5c5e07d6cd
        - Version: 2019 WFS gemeente_gegeneraliseerd
    - Natura2000_end2019_shp:
        - Link: https://www.eea.europa.eu/en/datahub/datahubitem-view/6fc8ad2d-195d-40f4-bdec-576e7d1268e4?activeAccordion=1091667,1070049
        - Version: 2019, Apr. 2020, SHP format
