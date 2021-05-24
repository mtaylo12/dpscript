#!/usr/bin/env python3

import networkx as nx
import geopandas as gp
from shapely.geometry import shape
import argparse
import os
import fiona 
import matplotlib.pyplot as plt

def graph_from_shp(filename):
    G = nx.Graph()
    data = gp.read_file(filename)
    # data.plot()
    # plt.show()

    for index, row in data.iterrows():
        xc = row["geometry"].centroid.x
        yc = row["geometry"].centroid.y
        
        G.add_node(index, coords=(xc,yc))

    blocks = fiona.open(filename)
    for count1, shp1 in enumerate(blocks):
        block1 = shape(shp1['geometry'])

        for count2, shp2 in enumerate(blocks):
            block2 = shape(shp1['geometry'])
            if(block1.intersects(block2)):
                G.add_edge(count1, count2)
            

    print('graph created')
    return G
    

p = argparse.ArgumentParser()
p.add_argument("shpfile", help="relative path to shapefile (should be in directory with other components)")

args = p.parse_args()
graph_from_shp(args.shpfile)


