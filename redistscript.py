#!/usr/bin/env python3

import sys
import os
import matplotlib.pyplot as plt
import networkx as nx

def createGraph(c, e, p):
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
    original_stdout = sys.stdout # Save a reference to the original standard output

    with open('example.co', 'w+') as f, open('examplePops','w+') as p:
        # f (.co file): node coordinates (row = node index)
        # p: populations corresponding to node indices

        for n in G:
            # setup .co file
            sys.stdout = f
            coords=nx.get_node_attributes(G,'coords')
            print(coords[n][0], coords[n][1])

            # setup pop file
            sys.stdout = p
            pop=nx.get_node_attributes(G,'pop')
            print(pop[n])

    with open('example.gr','w+') as g, open('exampleDarts','w+') as d:
        # g (.gr file): edge descriptions (row = edge index, numbers correspond to vertices)
        darts = [None]*G.number_of_nodes()
        for i, e in enumerate(G.edges):
            # setup edge file
            sys.stdout = g
            print(e[0],e[1])

            # setup dart data
            sys.stdout = d
            d1 = 2*i
            d2 = 2*i + 1
            d1_index = e[0]
            d2_index = e[1]

            if darts[d1_index] == None:
                darts[d1_index] = d1
            if darts[d2_index] == None:
                darts[d2_index] = d2

        print(*darts, sep = "\n")    
    sys.stdout = original_stdout # Reset the standard output to its original value

def main():
    assert(len(sys.argv) == 4)

    coordinate_file = sys.argv[1]
    population_file = sys.argv[2]
    edge_file = sys.argv[3]

    coordinates = ([(int(x.split()[0]),int(x.split()[1])) for x in open(coordinate_file).readlines()])
    edges = ([(int(x.split()[0]), int(x.split()[1])) for x in open(edge_file).readlines()])
    populations = ([int(x.split()[0]) for x in open(population_file).readlines()])

    # TODO: create 10% population bounds
    
    minpop = 150000
    maxpop = 300000

    # TODO: create district bounds
    mindist = 1
    maxdist = 10

    G = createGraph(coordinates, edges, populations)
    setup_inputs(G)
    
    command = "./redistricting example examplePops exampleDarts " + str(minpop) + " " + str(maxpop) + " " + str(mindist) + " " + str(maxdist)
    shell_out(command)

if __name__ == '__main__':
    main()
