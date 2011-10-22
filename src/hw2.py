#!/usr/bin/env python

import os
import networkx as nx
from collections import deque
import LT
import IC


filename = ('GrQc', 'HepPh', 'HepTh')
algorithm = ('lt', 'ic')
ratio = (0, 0.01, 0.02, 0.03, 0.04, 0.05)

for fn in filename:
    for algo in algorithm:
        for block_ratio in ratio:
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

            # read block node list from file
            block_list = []
            if block_ratio != 0:
                f = open('../part_b/'+algo+'_'+str(block_ratio)+'_ca-'+fn+'.txt', 'r')
                for line in f:
                    element = line.split()
                    block_list.append(element[0])

            # mark blocked
            for node in block_list:
                G.node[node]['blocked'] = True

            # do bfs
            if algo == 'lt':
                infected_node_num = LT.bfs(G, queue, infected_node_num)
            elif algo == 'ic':
                infected_node_num = IC.bfs(G, queue, infected_node_num)
            else:
                print 'Unknow algorithm'
                continue

            print '%s\t%s\t%.2f' % (fn, algo, block_ratio),
            print str(infected_node_num) + '/' + str(G.number_of_nodes()) + "  \t" + str(float(infected_node_num)/G.number_of_nodes())

            # check if dir exist
            if not os.path.isdir('output'):
                os.mkdir('output')
            if not os.path.isdir('output/part_a'):
                os.mkdir('output/part_a')

            if block_ratio == 0:
                # write infected nodes to output
                f = open('output/part_a/'+algo+'_ca-'+fn+'.txt', 'w')
                for node in G.nodes():
                    if G.node[node]['infected']:
                        f.write(node + "\n")
                f.close()

