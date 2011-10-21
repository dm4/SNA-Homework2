#!/usr/bin/env python

import os
import random
import networkx as nx
from collections import deque


#filename = ('GrQc', 'HepPh', 'HepTh')
#filename = ['dm4']
filename = ['GrQc', 'HepPh', 'HepTh', 'dm4']

for fn in filename:
    G = nx.DiGraph()
    queue = deque()

    # read graph
    f = open('../sn/ca-'+fn+'_clean.txt', 'r')
    for line in f:
        element = line.split()
        G.add_edge(element[0], element[1])
    f.close()

    # set uninfected and unblocked
    for node in G.nodes():
        G.node[node]['infected'] = False
        G.node[node]['blocked'] = False

    # read source node
    f = open('../source_v3/'+fn+'_reveal.txt', 'r')
    for line in f:
        element = line.split()
        G.node[element[0]]['infected'] = True
        queue.append(element[0])
    f.close()

    # initial infected node number
    infected_node_num = len(queue)

    # decide node to block
    block_list = []
    for node in G.nodes():
        if G.node[node]['infected']:
            continue
        else:
            weight = 0
            in_infected = 0
            for in_node in G.predecessors(node):
                if G.node[in_node]['infected']:
                    in_infected += 1
            weight = in_infected * 2 + G.out_degree(node)
            block_list.append({'node': node, 'weight': weight})
    block_list.sort(key=lambda x:x['weight'], reverse=True)

    block_ratio = 0.05
    print "block ratio " + str(block_ratio)
    # use first n block nodes
    block_list = block_list[:int(G.number_of_nodes() * block_ratio)]

    # mark blocked
    for b_node in block_list:
        G.node[b_node['node']]['blocked'] = True

    # do bfs
    while len(queue) > 0:
        node = queue.popleft()
        for nb in G.successors(node):
            if G.node[nb]['infected'] or G.node[nb]['blocked']:
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
    f = open('../part_b/ic_'+str(block_ratio)+'_ca-'+fn+'.txt', 'w')
    for node in G.nodes():
        if G.node[node]['infected']:
            f.write(node + "\n")
    f.close()

