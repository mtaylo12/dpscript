#!/usr/bin/env python3

import sys
import os
import matplotlib.pyplot as plt
import networkx as nx
import argparse
import re


def graph_from_txt(c, e, p):
    G = nx.Graph()
    G.add_nodes_from(c)
    G = nx.convert_node_labels_to_integers(G, first_label=0, ordering='default', label_attribute='coords')

    popdict = dict(zip(G.nodes(), p))
    nx.set_node_attributes(G,popdict, 'pop')
    G.add_edges_from(e)
    
    return G

def shell_out(str):
  r = os.system(str)
  if r != 0:
    raise Exception("command failed")

def list_average(list):
    return sum(list) / len(list)

def setup_inputs(G):

    #setup node and pop file
    node_file = open('/tmp/graph.co', 'w+') #node coordinates (row = node index)
    pop_file = open('/tmp/graphPops','w+') #populations corresponding to node indices
    for n in G:
        coords=nx.get_node_attributes(G,'coords')
        print(coords[n][0], coords[n][1], file=node_file)

        pop=nx.get_node_attributes(G,'pop')
        print(pop[n], file=pop_file)

    # setup edge and dart file
    edge_file = open('/tmp/graph.gr','w+') #row = edge index, values = vertices
    dart_file = open('/tmp/graphDarts','w+')
    darts = [None]*G.number_of_nodes()
    for i, e in enumerate(G.edges):
        print(e[0],e[1], file=edge_file)

        d1 = 2*i
        d2 = 2*i + 1
        d1_index = e[0]
        d2_index = e[1]

        if darts[d1_index] == None:
            darts[d1_index] = d1
        if darts[d2_index] == None:
            darts[d2_index] = d2

    print(*darts, sep = "\n", file = dart_file)    
    edge_file.close()
    dart_file.close()

def parse():
    p = argparse.ArgumentParser()
    p.add_argument("coordfile", help="text file of listed coordinates: [x y]")
    p.add_argument("popfile", help="text file of listed populations")
    p.add_argument("edgefile", help="text file of edges with numbered vertices: [vertex1 vertex2]")
    args = p.parse_args()
    return args.coordfile, args.popfile, args.edgefile

def graph_cut(G,cut_edges,edges):
    for i in cut_edges:
        x = edges[i][0]
        y = edges[i][1]
        G.remove_edge(x,y)
    return G

def main():
    [coordinate_file, population_file, edge_file] = parse()

    coordinates = ([(int(x.split()[0]),int(x.split()[1])) for x in open(coordinate_file).readlines()])
    edges = ([(int(x.split()[0]), int(x.split()[1])) for x in open(edge_file).readlines()])
    populations = ([int(x.split()[0]) for x in open(population_file).readlines()])

    # TODO: create 10% population bounds
    minpop = 150000
    maxpop = 300000

    # TODO: create district bounds
    mindist = 1
    maxdist = 10

    G = graph_from_txt(coordinates, edges, populations)
    
    # TODO: factor 
    setup_inputs(G)

    # TODO: check if planar
    # TODO: extract coords from graph directly

    plt.subplot(121)
    nx.draw_networkx(G, pos=dict(zip(G.nodes(),coordinates)))


    cut_file = open('/tmp/cut_edges.txt','w+')
    command = "./redistricting /tmp/graph /tmp/graphPops /tmp/graphDarts " + str(minpop) + " " + str(maxpop) + " " + str(mindist) + " " + str(maxdist) + " > /tmp/cut_edges.txt"
    shell_out(command)
    
    
    cut_edges_str = (cut_file.read().split(","))
    if (cut_edges_str[-1] == "\n"):
        cut_edges_str = cut_edges_str[0:-1]

    cut_edges = [int(x) for x in cut_edges_str]

    G_cut = graph_cut(G,cut_edges,edges)

    plt.subplot(122)
    nx.draw_networkx(G_cut, pos=dict(zip(G_cut.nodes(),coordinates)))
    plt.show()
    
if __name__ == '__main__':
    main()
