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
            if block_ratio == 0:
                block_list = []
            else:
                block_list = block_list[:int(G.number_of_nodes() * block_ratio)]

            # mark blocked
            for b_node in block_list:
                G.node[b_node['node']]['blocked'] = True

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
            if not os.path.isdir('../part_a'):
                os.mkdir('../part_a')
            if not os.path.isdir('../part_b'):
                os.mkdir('../part_b')

            # write infected nodes to output
            if block_ratio == 0:
                f = open('../part_a/'+algo+'_ca-'+fn+'.txt', 'w')
                for node in G.nodes():
                    if G.node[node]['infected']:
                        f.write(node + "\n")
                f.close()
            else:
                f = open('../part_b/'+algo+'_'+str(block_ratio)+'_ca-'+fn+'.txt', 'w')
                for node in G.nodes():
                    if G.node[node]['infected']:
                        f.write(node + "\n")
                f.close()

