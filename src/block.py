#!/usr/bin/env pytthon

import os
import networkx as nx

filename = ('GrQc', 'HepPh', 'HepTh')
ratio = (0.01, 0.02, 0.03, 0.04, 0.05)

for fn in filename:
    for block_ratio in ratio:
        G = nx.DiGraph()

        # read graph
        f = open('../sn/ca-'+fn+'_clean.txt', 'r')
        for line in f:
            element = line.split()
            G.add_edge(element[0], element[1])
        f.close()

        # set uninfected and unblocked
        for node in G.nodes():
            G.node[node]['infected'] = False

        # read source node
        f = open('../source_v3/'+fn+'_reveal.txt', 'r')
        for line in f:
            element = line.split()
            G.node[element[0]]['infected'] = True
        f.close()

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

        # use first n block nodes
        block_list = block_list[:int(G.number_of_nodes() * block_ratio)]

        # check if dir exist
        if not os.path.isdir('../part_b'):
            os.mkdir('../part_b')

        # write block node list to output
        for algo in ('lt', 'ic'):
            f = open('../part_b/'+algo+'_'+str(block_ratio)+'_ca-'+fn+'.txt', 'w')
            for node in block_list:
                f.write(node['node'] + "\n")
            f.close()

