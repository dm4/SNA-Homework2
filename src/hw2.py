#!/usr/bin/env python

import os
import networkx as nx
from collections import deque
import LT


filename = ('GrQc', 'HepPh', 'HepTh')

for fn in filename:
    G = nx.DiGraph()
    queue = deque()

    # read graph
    f = open('../sn/ca-'+fn+'_clean.txt', 'r')
    for line in f:
        element = line.split()
        G.add_edge(element[0], element[1])
    f.close()

    # set uninfected
    for node in G.nodes():
        G.node[node]['infected'] = False

    # read source node
    f = open('../source_v3/'+fn+'_reveal.txt', 'r')
    for line in f:
        element = line.split()
        G.node[element[0]]['infected'] = True
        queue.append(element[0])
    f.close()

    # initial infected node number
    infected_node_num = len(queue)

    # do bfs
    infected_node_num = LT.bfs(G, queue, infected_node_num)

    print fn + "\t" + str(infected_node_num) + '/' + str(G.number_of_nodes()) + "\t" + str(float(infected_node_num)/G.number_of_nodes())

    # check if ../part_a exist
    if not os.path.isdir('../part_a'):
        os.mkdir('../part_a')

    # write infected nodes to output
    f = open('../part_a/lt_ca-'+fn+'.txt', 'w')
    for node in G.nodes():
        if G.node[node]['infected']:
            f.write(node + "\n")
    f.close()

