#!/usr/bin/env python

import os
import random
import networkx as nx
from collections import deque


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
    while len(queue) > 0:
        node = queue.popleft()
        for nb in G.successors(node):
            if G.node[nb]['infected']:
                continue
            else:
                # check should be infected
                r = random.random()
                if r < 0.8:
                    G.node[nb]['infected'] = True
                    infected_node_num += 1
                    queue.append(nb)

    print fn + "\t" + str(infected_node_num) + '/' + str(G.number_of_nodes()) + "\t" + str(float(infected_node_num)/G.number_of_nodes())

    # check if ../part_a exist
    if not os.path.isdir('../part_a'):
        os.mkdir('../part_a')

    # write infected nodes to output
    f = open('../part_a/ic_ca-'+fn+'.txt', 'w')
    for node in G.nodes():
        if G.node[node]['infected']:
            f.write(node + "\n")
    f.close()

